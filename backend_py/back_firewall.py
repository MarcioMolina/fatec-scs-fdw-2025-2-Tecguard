#!/usr/bin/env python3
import sys
import json
import re
import hashlib
import threading
import time
import psutil
import platform
import requests
from datetime import datetime, timedelta
from scapy.all import sniff, IP, TCP, UDP, Raw, get_if_list
from scapy.layers.tls.all import TLS
from PySide6.QtCore import QObject, Signal
import yara
import subprocess
from pybloom_live import ScalableBloomFilter
import os
import numpy as np
from scapy.layers.tls.all import *
import pandas as pd
from collections import defaultdict
from PySide6.QtWidgets import QMessageBox
from typing import Optional, Dict, Any

class JSONLogger:
    """Logger personalizado que gera logs em formato JSON com estrutura padronizada"""
    
    def __init__(self, log_file: str = "firewall_logs.json"):
        self.log_file = log_file
        # Cria o arquivo de log se não existir
        open(self.log_file, 'a').close()
    
    def _log(self, event_name: str, classification: str, 
             ip: Optional[str] = None, port: Optional[int] = None,
             service: Optional[str] = None, suggestion: Optional[str] = None,
             additional_data: Optional[Dict[str, Any]] = None):
        """Método interno para gerar logs formatados"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_name,
            "classification": classification,
            "ip": ip,
            "port": port,
            "service": service,
            "suggestion": suggestion,
            "additional_data": additional_data or {}
        }
        
        # Remove campos vazios para economizar espaço
        log_entry = {k: v for k, v in log_entry.items() if v is not None and v != {}}
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Falha ao escrever no log: {str(e)}")

    def info(self, event_name: str, **kwargs):
        """Log informativo"""
        self._log(event_name, "Informativo", **kwargs)
    
    def error(self, event_name: str, **kwargs):
        """Log de erro"""
        self._log(event_name, "Erro", **kwargs)
    
    def warning(self, event_name: str, **kwargs):
        """Log de alerta"""
        self._log(event_name, "Alerta", **kwargs)
    
    def attack(self, event_name: str, **kwargs):
        """Log de ataque detectado"""
        self._log(event_name, "Ataque", **kwargs)
    
    def suspicious(self, event_name: str, **kwargs):
        """Log de atividade suspeita"""
        self._log(event_name, "Suspeito", **kwargs)

class YaraAnalyzer:
    """Analisador de pacotes usando regras YARA"""
    
    def __init__(self, firewall):
        self.firewall = firewall
        self._signature_cache = {}
        self._cache_lock = threading.Lock()
        self._init_yara_scanner()
        
    def _init_yara_scanner(self):
        """Inicia o motor de detecção baseado em YARA"""
        self.yara_rules = yara.compile(source='''
            rule BruteForce_SSH {
                meta:
                    description = "Tentativas de brute force SSH"
                strings:
                     $s1 = "Failed password for"
                $s2 = "authentication failure"
                $s3 = "invalid user"
                $s4 = "connection closed by"
                condition:
                    any of them
            }

            rule Web_Attack {
                strings:
                    $sqli = /union[\\s\\+]+select/i
                    $sqli2 = /select.*from/i
                    $xss = /<script[\\s>]/ nocase
                    $xss2 = /javascript:/ nocase
                    $xss3 = /onerror=/ nocase
                condition:
                    any of them
            }
                             
            rule DDoS_Attack_Indicators {
                meta:
                    description = "Detecta possíveis scripts/tools de DDoS (LOIC, HOIC, Slowloris, etc.)"
                    severity = "critical"          
            strings:
                // Padrões em scripts de DDoS (Python, Bash, etc.)
                $loic = "LOIC" nocase
                $hoic = "HOIC" nocase
                $slowloris = "slowloris" nocase
                $udp_flood = "udpflood" nocase
                $syn_flood = "synflood" nocase
                $http_flood = "httpflood" nocase

                // Strings comuns em ferramentas de DDoS
                $target_url = "TARGET_URL"
                $target_ip = "TARGET_IP"
                $attack_duration = "ATTACK_DURATION"
                $threads = "THREADS"

                // Códigos maliciosos (exemplo simplificado)
                $python_attack = "import socket"
                $bash_attack = "hping3"

            condition:
                // Pelo menos 3 desses indicadores
                3 of them
        }            
            ''')
    
    def analyze(self, pkt):
        """Análise de payload com regras YARA"""
        if not pkt.haslayer(Raw):
            return None
            
        try:
            payload = pkt[Raw].load
            if not payload:
                return None
                
            # Verifica em cache primeiro
            payload_hash = hashlib.md5(payload).hexdigest()
            with self._cache_lock:
                if payload_hash in self._signature_cache:
                    cached_result = self._signature_cache[payload_hash]
                    if cached_result['expire'] > time.time():
                        return cached_result['result']
            
            # Executa análise YARA
            matches = self.yara_rules.match(data=payload)
            if matches:
                self.firewall.stats['yara_matches'] += 1
                
                # Classifica severidade baseada nas regras
                severity_scores = {
                    'critical': 100,
                    'high': 80,
                    'medium': 50,
                    'low': 30
                }
                
                max_score = 0
                reasons = []
                details = {'rules': []}
                
                for match in matches:
                    rule_severity = match.meta.get('severity', 'medium').lower()
                    score = severity_scores.get(rule_severity, 50)
                    
                    if score > max_score:
                        max_score = score
                    
                    reasons.append(match.rule)
                    details['rules'].append({
                        'name': match.rule,
                        'severity': rule_severity,
                        'description': match.meta.get('description', '')
                    })
                
                result = {
                    'block': max_score >= 80,
                    'reason': f"Regras YARA: {', '.join(reasons)}",
                    'score': max_score,
                    'details': details
                }
                
                # Log do evento
                src_ip = pkt[IP].src if pkt.haslayer(IP) else None
                self.firewall.logger.attack(
                    "Assinatura YARA detectada",
                    ip=src_ip,
                    service="Deep Packet Inspection",
                    suggestion="Analisar payload e considerar bloqueio",
                    additional_data={
                        'rules': reasons,
                        'score': max_score,
                        'payload_hash': payload_hash
                    }
                )
                
                # Cache resultado por 1 hora
                with self._cache_lock:
                    self._signature_cache[payload_hash] = {
                        'result': result,
                        'expire': time.time() + 3600
                    }
                    
                return result
                
        except Exception as e:
            self.firewall.logger.error(
                "Erro na análise YARA",
                service="YaraAnalyzer",
                suggestion="Verificar integridade das regras YARA",
                additional_data={'error': str(e)}
            )
            
        return None

class JA3Analyzer:
    """Analisador de fingerprints TLS com JA3"""
    
    def __init__(self, firewall):
        self.firewall = firewall
        self._signature_cache = {}
        self._cache_lock = threading.Lock()
    
    def analyze(self, pkt):
        """Análise de fingerprint TLS com JA3"""
        if not pkt.haslayer(TLS):
            return None
            
        try:
            ja3_hash = self._calculate_ja3(pkt[TLS])
            if not ja3_hash:
                return None
                
            # Verifica no banco de dados JA3
            is_malicious = self.firewall.ja3_db.is_malicious(ja3_hash)
            if is_malicious:
                self.firewall.stats['ja3_matches'] += 1
                
                src_ip = pkt[IP].src if pkt.haslayer(IP) else None
                self.firewall.logger.attack(
                    "Fingerprint JA3 malicioso detectado",
                    ip=src_ip,
                    service="TLS Inspection",
                    suggestion="Bloquear IP imediatamente",
                    additional_data={'ja3_hash': ja3_hash}
                )
                
                return {
                    'block': True,
                    'reason': f"Fingerprint JA3 malicioso: {ja3_hash}",
                    'score': 90,
                    'details': {'ja3': ja3_hash}
                }
                
            # Verifica em cache local de anomalias
            with self._cache_lock:
                if ja3_hash in self._signature_cache:
                    cached_result = self._signature_cache[ja3_hash]
                    if cached_result['expire'] > time.time():
                        return cached_result['result']
            
            # Verificação adicional para anomalias
            anomaly_result = self._check_ja3_anomalies(pkt[TLS], ja3_hash)
            if anomaly_result:
                # Log de anomalia
                src_ip = pkt[IP].src if pkt.haslayer(IP) else None
                self.firewall.logger.suspicious(
                    "Anomalia TLS detectada",
                    ip=src_ip,
                    service="TLS Inspection",
                    suggestion="Investigar conexão",
                    additional_data=anomaly_result['details']
                )
                
                # Cache resultado por 1 hora
                with self._cache_lock:
                    self._signature_cache[ja3_hash] = {
                        'result': anomaly_result,
                        'expire': time.time() + 3600
                    }
                return anomaly_result
                
        except Exception as e:
            self.firewall.logger.error(
                "Erro na análise JA3",
                service="JA3Analyzer",
                suggestion="Verificar integridade do banco de dados JA3",
                additional_data={'error': str(e)}
            )
            
        return None
    
    def _calculate_ja3(self, tls_layer):
        """Cálculo JA3 com tratamento completo de erros"""
        try:
            # Verificação da estrutura TLS
            if not tls_layer or not hasattr(tls_layer, 'msg'):
                return None

            # Encontra o Client Hello
            client_hello = next(
                (msg for msg in tls_layer.msg 
                if hasattr(msg, 'msgtype') and msg.msgtype == 1),
                None
            )
            if not client_hello:
                return None

            # Obtém versão TLS com fallback seguro
            version = getattr(client_hello, 'version', '769')  # 769 = TLS 1.0 como fallback
            
            # Processa cifras válidas
            ciphers = []
            if hasattr(client_hello, 'ciphers'):
                ciphers = [
                    str(c) for c in client_hello.ciphers 
                    if isinstance(c, int) and 0x0000 < c <= 0xFFFF
                ]

            # Processa extensões
            extensions = []
            if hasattr(client_hello, 'extensions'):
                extensions = [
                    str(e.type) for e in client_hello.extensions 
                    if hasattr(e, 'type')
                ]

            # Constrói string JA3
            ja3_str = f"{version}," \
                    f"{'-'.join(ciphers) if ciphers else ''}," \
                    f"{'-'.join(extensions) if extensions else ''}"

            return hashlib.md5(ja3_str.encode()).hexdigest()

        except Exception as e:
            self.firewall.logger.error(
                "Erro no cálculo do JA3",
                service="JA3Analyzer",
                suggestion="Verificar pacote TLS",
                additional_data={'error': str(e)}
            )
            return None
    
    def _check_ja3_anomalies(self, tls_layer, ja3_hash):
        """Verifica anomalias em fingerprints JA3"""
        try:
            client_hello = next(
                (msg for msg in tls_layer.msg 
                if hasattr(msg, 'msgtype') and msg.msgtype == 1),
                None
            )
            if not client_hello:
                return None
                
            # Verifica versões TLS obsoletas
            if hasattr(client_hello, 'version'):
                tls_version = client_hello.version
                if tls_version < 0x0303:  # Antes do TLS 1.2
                    return {
                        'block': False,
                        'reason': f"Versão TLS obsoleta: {tls_version}",
                        'score': 40,
                        'details': {
                            'ja3': ja3_hash,
                            'tls_version': tls_version
                        }
                    }
            
            # Verifica cifras inseguras
            if hasattr(client_hello, 'ciphers'):
                weak_ciphers = {
                    0x0000: 'NULL',
                    0x0005: 'RC4',
                    0x000A: 'DES',
                    0x002F: 'AES-CBC',
                    0x0030: 'AES-GCM',
                    0x0004: 'RC4-40'
                }
                
                weak_in_use = [
                    weak_ciphers[c] for c in client_hello.ciphers 
                    if c in weak_ciphers
                ]
                
                if weak_in_use:
                    return {
                        'block': False,
                        'reason': f"Cifras fracas detectadas: {', '.join(weak_in_use)}",
                        'score': 60,
                        'details': {
                            'ja3': ja3_hash,
                            'weak_ciphers': weak_in_use
                        }
                    }
                    
        except Exception as e:
            self.firewall.logger.error(
                "Erro na verificação de anomalias JA3",
                service="JA3Analyzer",
                suggestion="Verificar pacote TLS",
                additional_data={'error': str(e)}
            )
            
        return None

class StatisticalAnalyzer:
    """Analisador estatístico de tráfego"""
    
    def __init__(self, firewall):
        self.firewall = firewall
        self.http_patterns = {
            "sqli": re.compile(r"('|\"|%27).*(OR|AND|SELECT|UNION|WHERE)", re.IGNORECASE),
            "xss": re.compile(r"<script.*?>|javascript:", re.IGNORECASE),
            "webshell": re.compile(r"cmd\.exe|/bin/sh|wget\s+http", re.IGNORECASE)
        }
    
    def analyze(self, pkt):
        """Análise de metadados para detecção de padrões suspeitos"""
        if not pkt.haslayer(IP):
            return None
            
        result = {'score': 0, 'details': {}}
        src_ip = pkt[IP].src
        
        # 1. Verificação de portscan
        portscan_result = self._check_portscan(pkt, src_ip)
        if portscan_result:
            result['score'] += portscan_result.get('score', 0)
            result['details'].update(portscan_result.get('details', {}))
            if portscan_result.get('block', False):
                result['block'] = True
                result['reason'] = portscan_result.get('reason', '')
        
        # 2. Verificação de DDoS
        ddos_result = self._check_ddos(pkt, src_ip)
        if ddos_result:
            result['score'] += ddos_result.get('score', 0)
            result['details'].update(ddos_result.get('details', {}))
            if ddos_result.get('block', False):
                result['block'] = True
                if 'reason' in result:
                    result['reason'] += "; " + ddos_result.get('reason', '')
                else:
                    result['reason'] = ddos_result.get('reason', '')
        
        # 3. Verificação de protocolos incomuns
        proto_result = self._check_unusual_protocols(pkt)
        if proto_result:
            result['score'] += proto_result.get('score', 0)
            result['details'].update(proto_result.get('details', {}))
        
        # 4. Verificação DPI
        dpi_result = self._analyze_dpi(pkt)
        if dpi_result:
            result['score'] += dpi_result.get('score', 0)
            result['details'].update(dpi_result.get('details', {}))
            if dpi_result.get('block', False):
                result['block'] = True
                if 'reason' in result:
                    result['reason'] += "; " + dpi_result.get('reason', '')
                else:
                    result['reason'] = dpi_result.get('reason', '')
        
        return result if result['score'] > 0 else None
    
    def _check_portscan(self, pkt, src_ip):
        """Detecção de portscan com estado"""
        if not pkt.haslayer(TCP):
            return None
            
        dst_port = pkt[TCP].dport
        conn_key = (src_ip, pkt[IP].dst)
        
        with self.firewall.flow_lock:
            # Atualiza estatísticas de conexão
            if conn_key not in self.firewall.flow_cache:
                self.firewall.flow_cache[conn_key] = {
                    'ports': set(),
                    'count': 0,
                    'start_time': time.time()
                }
                
            conn = self.firewall.flow_cache[conn_key]
            conn['count'] += 1
            conn['ports'].add(dst_port)
            
            # Critérios para portscan
            if len(conn['ports']) > 5 and conn['count'] > 10:
                current_time = time.time()
                scan_rate = len(conn['ports']) / (current_time - conn['start_time'])
                
                if scan_rate > 2:  # Mais de 2 portas/segundo
                    # Log do portscan
                    self.firewall.logger.suspicious(
                        "Port scan detectado",
                        ip=src_ip,
                        port=list(conn['ports'])[0],  # Mostra a primeira porta
                        service="Network",
                        suggestion="Investigar origem e considerar bloqueio",
                        additional_data={
                            'port_count': len(conn['ports']),
                            'scan_rate': f"{scan_rate:.2f} ports/sec",
                            'target_ip': pkt[IP].dst
                        }
                    )
                    
                    return {
                        'block': True,
                        'reason': f"Possível port scan ({len(conn['ports'])} portas em {conn['count']} pacotes)",
                        'score': 80,
                        'details': {
                            'ports': list(conn['ports']),
                            'scan_rate': f"{scan_rate:.2f} ports/sec"
                        }
                    }
        
        return None
    
    def _check_ddos(self, pkt, src_ip):
        """Detecção de DDoS baseada em taxa e volume"""
        current_time = time.time()
        pkt_len = len(pkt)
        
        with self.firewall.flow_lock:
            # Inicializa estatísticas se necessário
            if src_ip not in self.firewall.ddos_stats:
                self.firewall.ddos_stats[src_ip] = {
                    'count': 0,
                    'total_size': 0,
                    'start_time': current_time,
                    'last_pkt_time': current_time
                }
                
            stats = self.firewall.ddos_stats[src_ip]
            
            # Reseta contador se a janela expirou (1 segundo)
            if current_time - stats['start_time'] > 1.0:
                stats['count'] = 0
                stats['total_size'] = 0
                stats['start_time'] = current_time
            
            # Atualiza estatísticas
            stats['count'] += 1
            stats['total_size'] += pkt_len
            stats['last_pkt_time'] = current_time
            
            # Calcula taxas
            pkt_rate = stats['count'] / (current_time - stats['start_time'] + 0.001)
            bandwidth = stats['total_size'] / (current_time - stats['start_time'] + 0.001)
            
            # Verifica limites
            score = 0
            reasons = []
            
            if pkt_rate > self.firewall.ddos_thresholds['packet_rate']:
                score += 60
                reasons.append(f"Alta taxa de pacotes ({pkt_rate:.1f} pps)")
                
            if bandwidth > self.firewall.ddos_thresholds['bandwidth']:
                score += 70
                reasons.append(f"Alto consumo de banda ({bandwidth/1e6:.2f} Mbps)")
            
            if pkt.haslayer(TCP) and pkt[TCP].flags == 'S':
                if 'syn_count' not in stats:
                    stats['syn_count'] = 0
                stats['syn_count'] += 1
                
                syn_rate = stats['syn_count'] / (current_time - stats['start_time'] + 0.001)
                if syn_rate > self.firewall.ddos_thresholds['syn_rate']:
                    score += 90
                    reasons.append(f"SYN flood detectado ({syn_rate:.1f} SYN/s)")
            
            if score > 0:
                # Log do DDoS
                self.firewall.logger.attack(
                    "Possível ataque DDoS detectado",
                    ip=src_ip,
                    service="Network",
                    suggestion="Ativar mitigação DDoS",
                    additional_data={
                        'pkt_rate': pkt_rate,
                        'bandwidth': bandwidth,
                        'flags': str(pkt[TCP].flags) if pkt.haslayer(TCP) else None
                    }
                )
                
                return {
                    'block': score >= 80,
                    'reason': "; ".join(reasons),
                    'score': score,
                    'details': {
                        'pkt_rate': pkt_rate,
                        'bandwidth': bandwidth,
                        'packet_size': pkt_len
                    }
                }
        
        return None
    
    def _check_unusual_protocols(self, pkt):
        """Detecta protocolos incomuns ou configurações suspeitas"""
        if not pkt.haslayer(IP):
            return None
            
        score = 0
        details = {}
        
        # Verifica protocolos incomuns
        if pkt[IP].proto not in [6, 17]:  # Não é TCP/UDP
            score += 30
            details['unusual_proto'] = pkt[IP].proto
            
        # Verifica portas suspeitas
        if pkt.haslayer(TCP):
            dport = pkt[TCP].dport
            if dport in [4444, 31337, 6667]:  # Portas comuns de backdoors
                score += 50
                details['suspicious_port'] = dport
                
        elif pkt.haslayer(UDP):
            dport = pkt[UDP].dport
            if dport in [53, 123, 161, 1900]:  # Potenciais para amplificação
                if len(pkt) > 500:  # Pacotes grandes
                    score += 60
                    details['udp_amplification'] = {
                        'port': dport,
                        'size': len(pkt)
                    }
        
        if score > 0:
            # Log de protocolo incomum
            self.firewall.logger.suspicious(
                "Protocolo ou porta incomum detectada",
                ip=pkt[IP].src,
                port=dport if 'dport' in locals() else None,
                service="Network",
                suggestion="Verificar tráfego",
                additional_data=details
            )
        
        return {'score': score, 'details': details} if score > 0 else None
    
    def _analyze_dpi(self, pkt):
        """Deep Packet Inspection para protocolos específicos"""
        if not pkt.haslayer(Raw):
            return None
            
        try:
            raw_data = pkt[Raw].load
            if not raw_data:
                return None
                
            # Verifica protocolo HTTP
            if b"HTTP/" in raw_data or b"GET " in raw_data or b"POST " in raw_data:
                return self._analyze_http(pkt, raw_data)
                
            # Verifica protocolo DNS
            if pkt.haslayer(UDP) and pkt[UDP].dport == 53:
                return self._analyze_dns(pkt, raw_data)
                
        except Exception as e:
            self.firewall.logger.error(
                "Erro na análise DPI",
                service="StatisticalAnalyzer",
                suggestion="Verificar pacote",
                additional_data={'error': str(e)}
            )
            
        return None
    
    def _analyze_http(self, pkt, raw_data):
        """Análise profunda de tráfego HTTP"""
        try:
            payload_str = raw_data.decode(errors='ignore')
            result = {'score': 0, 'details': {}}
            
            # Verifica User-Agent suspeitos
            if "User-Agent:" in payload_str:
                user_agent = payload_str.split("User-Agent:")[1].split("\r\n")[0].strip()
                if self._is_malicious_user_agent(user_agent):
                    result['score'] += 70
                    result['details']['malicious_ua'] = user_agent
                    result['reason'] = f"User-Agent malicioso: {user_agent}"
            
            # Verifica padrões de ataque
            for threat_type, pattern in self.http_patterns.items():
                if pattern.search(payload_str):
                    result['score'] += 80
                    if 'reason' in result:
                        result['reason'] += f"; Ataque {threat_type.upper()} detectado"
                    else:
                        result['reason'] = f"Ataque {threat_type.upper()} detectado"
                    result['details'][threat_type] = True
                    result['block'] = True
            
            # Verifica caminhos suspeitos
            suspicious_paths = [
                r'/admin', r'/wp-admin', r'/console', 
                r'/\.env', r'/phpmyadmin', r'/\.git'
            ]
            
            for path in suspicious_paths:
                if re.search(rf'GET\s+{path}', payload_str, re.I):
                    result['score'] += 50
                    if 'reason' in result:
                        result['reason'] += f"; Acesso a caminho suspeito: {path}"
                    else:
                        result['reason'] = f"Acesso a caminho suspeito: {path}"
                    result['details']['suspicious_path'] = path
            
            if result['score'] > 0:
                # Log de ataque HTTP
                self.firewall.logger.attack(
                    "Ataque HTTP detectado",
                    ip=pkt[IP].src,
                    port=pkt[TCP].dport if pkt.haslayer(TCP) else None,
                    service="HTTP",
                    suggestion="Bloquear origem e investigar",
                    additional_data=result['details']
                )
            
            return result if result['score'] > 0 else None
            
        except Exception as e:
            self.firewall.logger.error(
                "Erro na análise HTTP",
                service="StatisticalAnalyzer",
                suggestion="Verificar pacote HTTP",
                additional_data={'error': str(e)}
            )
            return None
    
    def _analyze_dns(self, pkt, raw_data):
        """Análise de tráfego DNS para tunneling ou exfiltração"""
        try:
            # Implementação básica - pode ser expandida
            dns_query = raw_data[12:].split(b'\x00', 1)[0]
            query_str = dns_query.decode('ascii', errors='ignore')
            
            # Verifica domínios suspeitos
            suspicious_domains = [
                r'dynamic-dns\.net$',
                r'no-ip\.com$',
                r'ddns\.net$',
                r'tunnel\.com$'
            ]
            
            for domain in suspicious_domains:
                if re.search(domain, query_str, re.I):
                    # Log de DNS suspeito
                    self.firewall.logger.suspicious(
                        "Consulta DNS suspeita",
                        ip=pkt[IP].src,
                        port=53,
                        service="DNS",
                        suggestion="Investigar origem",
                        additional_data={
                            'query': query_str,
                            'matched_pattern': domain
                        }
                    )
                    
                    return {
                        'block': False,
                        'reason': f"Consulta DNS suspeita: {query_str}",
                        'score': 60,
                        'details': {
                            'dns_query': query_str,
                            'suspicious_domain': domain
                        }
                    }
                    
        except Exception as e:
            self.firewall.logger.error(
                "Erro na análise DNS",
                service="StatisticalAnalyzer",
                suggestion="Verificar pacote DNS",
                additional_data={'error': str(e)}
            )
            
        return None
    
    def _is_malicious_user_agent(self, user_agent):
        """Verifica User-Agents maliciosos"""
        malicious_agents = [
            "sqlmap", "nmap", "metasploit", 
            "nikto", "wget", "curl", "havij",
            "hydra", "nessus", "burp", "zap",
            "w3af", "arachni", "skipfish"
        ]
        return any(agent in user_agent.lower() for agent in malicious_agents)

class AnalysisPipeline:
    """Pipeline de análise com early termination e priorização de etapas"""
    
    def __init__(self, firewall):
        self.firewall = firewall
        
        # Inicializa os analisadores
        self.yara_analyzer = YaraAnalyzer(firewall)
        self.ja3_analyzer = JA3Analyzer(firewall)
        self.statistical_analyzer = StatisticalAnalyzer(firewall)
        
        # Inicializa o AIAnalyzer apenas se o ai_chooser estiver disponível
        self.ai_analyzer = None
        if hasattr(firewall, 'ai_chooser') and firewall.ai_chooser is not None:
            self.ai_analyzer = AIAnalyzer(firewall, firewall.ai_chooser)

        if self.ai_analyzer is not None and not getattr(firewall, 'gamer_mode', False):
            self.steps.append(self.ai_analyzer.analyze)
        
        # Define a ordem de execução dos analisadores
        self.steps = [
            self._check_blocked_ips,
            self.statistical_analyzer.analyze,
            self.ja3_analyzer.analyze,
            self.yara_analyzer.analyze
        ]
        
        # Adiciona o analisador de IA apenas se estiver disponível
        if self.ai_analyzer is not None:
            self.steps.append(self.ai_analyzer.analyze)
        
        # Sistema de scoring
        self.thresholds = {
            'critical': 100,
            'high': 80,
            'medium': 50,
            'low': 30
        }
        
        # Cache para otimização
        self._signature_cache = {}
        self._cache_lock = threading.Lock()
        
    
    def process_packet(self, pkt):
        """Processa o pacote através do pipeline com early termination"""
        result = {
            'block': False,
            'reason': [],
            'score': 0,
            'details': {}
        }
        
        for step in self.steps:
            try:
                step_result = step(pkt)
                if step_result:
                    # Atualiza resultado com informações da etapa
                    result['score'] += step_result.get('score', 0)
                    if step_result.get('block', False):
                        result['block'] = True
                    if 'reason' in step_result:
                        result['reason'].append(step_result['reason'])
                    if 'details' in step_result:
                        result['details'].update(step_result['details'])
                    
                    # Early termination se for crítica
                    if result['score'] >= self.thresholds['critical']:
                        break
                        
            except Exception as e:
                self.firewall.logger.error(
                    "Erro no pipeline de análise",
                    service="AnalysisPipeline",
                    suggestion="Verificar analisador específico",
                    additional_data={
                        'step': step.__name__,
                        'error': str(e)
                    }
                )
        
        # Toma decisão baseada no score acumulado
        if not result['block'] and result['score'] >= self.thresholds['high']:
            result['block'] = True
            result['reason'].append(f"Score acumulado alto: {result['score']}")
        
        return result
    
    def _check_blocked_ips(self, pkt):
        """Verificação ultra-rápida de IPs bloqueados"""
        if not pkt.haslayer(IP):
            return None

        src_ip = pkt[IP].src
        
        # Verifica cache rápido
        if self.firewall.acl_manager.is_blocked(src_ip):
            self.firewall.logger.info(
                "Pacote de IP bloqueado descartado",
                ip=src_ip,
                service="ACL"
            )
            return {
                'block': True,
                'reason': 'IP bloqueado via ACL',
                'score': 100,
                'details': {'ip': src_ip, 'stage': 'pre-filter'}
            }
            
        return None
    
class NetworkFeatureExtractor:
    """Extrator aprimorado de features de rede"""
    
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.flows = {}
        self.lock = threading.Lock()
        
    def packet_to_features(self, pkt):
        """Extrai features de um único pacote"""
        if not pkt.haslayer(IP):
            return None
            
        features = {
            'timestamp': time.time(),
            'src_ip': pkt[IP].src,
            'dst_ip': pkt[IP].dst,
            'protocol': pkt[IP].proto,
            'length': len(pkt),
            'is_tcp': 1 if pkt.haslayer(TCP) else 0,
            'is_udp': 1 if pkt.haslayer(UDP) else 0,
            'has_payload': 1 if pkt.haslayer(Raw) else 0
        }
        
        if pkt.haslayer(TCP):
            features.update({
                'src_port': pkt[TCP].sport,
                'dst_port': pkt[TCP].dport,
                'tcp_flags': str(pkt[TCP].flags),
                'tcp_window': pkt[TCP].window,
                'tcp_urgptr': pkt[TCP].urgptr
            })
        elif pkt.haslayer(UDP):
            features.update({
                'src_port': pkt[UDP].sport,
                'dst_port': pkt[UDP].dport
            })
            
        return features
    
    def update_flow_stats(self, pkt):
        """Atualiza estatísticas de fluxo para um pacote"""
        if not pkt.haslayer(IP):
            return
            
        flow_key = self._get_flow_key(pkt)
        if not flow_key:
            return
            
        with self.lock:
            if flow_key not in self.flows:
                self.flows[flow_key] = {
                    'start_time': time.time(),
                    'packet_count': 0,
                    'total_bytes': 0,
                    'packet_lengths': [],
                    'inter_arrivals': [],
                    'last_time': time.time(),
                    'flags': set()
                }
                
            flow = self.flows[flow_key]
            
            # Atualiza estatísticas
            current_time = time.time()
            pkt_len = len(pkt)
            
            flow['packet_count'] += 1
            flow['total_bytes'] += pkt_len
            flow['packet_lengths'].append(pkt_len)
            flow['inter_arrivals'].append(current_time - flow['last_time'])
            flow['last_time'] = current_time
            
            if pkt.haslayer(TCP):
                flow['flags'].add(pkt[TCP].flags)
                
            # Mantém apenas o tamanho da janela
            if len(flow['packet_lengths']) > self.window_size:
                flow['packet_lengths'] = flow['packet_lengths'][-self.window_size:]
                flow['inter_arrivals'] = flow['inter_arrivals'][-self.window_size:]
    
    def get_flow_features(self, flow_key):
        """Obtém features consolidadas de um fluxo"""
        with self.lock:
            if flow_key not in self.flows:
                return None
                
            flow = self.flows[flow_key]
            
            # Calcula estatísticas
            if not flow['packet_lengths']:
                return None
                
            mean_pkt_len = np.mean(flow['packet_lengths'])
            std_pkt_len = np.std(flow['packet_lengths'])
            mean_iat = np.mean(flow['inter_arrivals'])
            std_iat = np.std(flow['inter_arrivals'])
            duration = flow['last_time'] - flow['start_time']
            byte_rate = flow['total_bytes'] / duration if duration > 0 else 0
            pkt_rate = flow['packet_count'] / duration if duration > 0 else 0
            
            features = {
                'flow_duration': duration,
                'total_packets': flow['packet_count'],
                'total_bytes': flow['total_bytes'],
                'mean_pkt_len': mean_pkt_len,
                'std_pkt_len': std_pkt_len,
                'mean_iat': mean_iat,
                'std_iat': std_iat,
                'byte_rate': byte_rate,
                'pkt_rate': pkt_rate,
                'unique_flags': len(flow['flags']),
                'src_ip': flow_key[0],
                'dst_ip': flow_key[1],
                'src_port': flow_key[2],
                'dst_port': flow_key[3],
                'protocol': flow_key[4]
            }
            
            return features
    
    def get_feature_dataframe(self):
        """Consolida os dados dos fluxos em um DataFrame para análise em lote"""
        with self.lock:
            data = []
            for flow_key in self.flows:
                features = self.get_flow_features(flow_key)
                if features:
                    data.append(features)
                
            if not data:
                return pd.DataFrame()
            
            return pd.DataFrame(data)
            
    def _get_flow_key(self, pkt):
        """Gera uma chave única para o fluxo"""
        if not pkt.haslayer(IP):
            return None
            
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        proto = pkt[IP].proto
        
        if pkt.haslayer(TCP):
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport
        elif pkt.haslayer(UDP):
            src_port = pkt[UDP].sport
            dst_port = pkt[UDP].dport
        else:
            src_port = 0
            dst_port = 0
            
        return (src_ip, dst_ip, src_port, dst_port, proto)

class AIAnalyzer:
    """Realiza análises de pacotes usando o modelo de IA selecionado"""
    
    def __init__(self, firewall, ai_chooser):
        self.firewall = firewall
        self.extractor = NetworkFeatureExtractor()
        self.ai_chooser = ai_chooser
        self.model_status = {
            'loaded': False,
            'last_check': None,
            'error_count': 0
        }

    def _verify_model_loaded(self):
        """Verifica e valida se o modelo está carregado corretamente"""
        try:
            # Atualiza status
            self.model_status['last_check'] = datetime.now()
            
            model = self.ai_chooser.get_current_model()
            if model is None:
                self.model_status['loaded'] = False
                self.model_status['error_count'] += 1
                self.firewall.logger.error(
                    "Modelo de IA não disponível",
                    service="AIAnalyzer",
                    suggestion="Carregar modelo válido"
                )
                return False
                
            # Testa se o modelo tem os métodos necessários
            if not (hasattr(model, 'predict') and hasattr(model, 'predict_proba')):
                self.model_status['loaded'] = False
                self.model_status['error_count'] += 1
                self.firewall.logger.error(
                    "Modelo de IA incompatível",
                    service="AIAnalyzer",
                    suggestion="Verificar implementação do modelo"
                )
                return False
                
            # Verificação adicional para modelos específicos
            try:
                # Teste de predição vazia para validação
                dummy_data = np.zeros((1, 10))  # Tamanho arbitrário para teste
                model.predict(dummy_data)
                
                self.model_status['loaded'] = True
                return True
                
            except Exception as test_error:
                self.model_status['loaded'] = False
                self.model_status['error_count'] += 1
                self.firewall.logger.error(
                    "Falha na validação do modelo",
                    service="AIAnalyzer",
                    suggestion="Verificar modelo corrompido",
                    additional_data={'error': str(test_error)}
                )
                return False
                
        except Exception as e:
            self.model_status['loaded'] = False
            self.model_status['error_count'] += 1
            self.firewall.logger.error(
                "Erro na verificação do modelo",
                service="AIAnalyzer",
                suggestion="Verificar dependências",
                additional_data={'error': str(e)}
            )
            return False
        
    def get_model_status(self):
        """Retorna o status atual do modelo e verifica seu estado"""
        # Atualiza o status verificando o modelo
        self._verify_model_loaded()
        
        # Obtém cópia do status atual
        status = self.model_status.copy()
        
        # Adiciona mensagem descritiva baseada no status
        if not status['loaded']:
            status['message'] = "⚠️ Modelo não carregado ou inválido"
        else:
            status['message'] = "✅ Modelo carregado e válido"
        
        return status
    
    def analyze(self, pkt):
        """Análise usando modelo de IA"""
        try:
            # Extrai features do pacote
            features = self.extractor.packet_to_features(pkt)
            if not features:
                return None
                
            # Converte para DataFrame
            df = pd.DataFrame([features])
            
            # Obtém o modelo atual do AIChooser
            model = self.ai_chooser.get_current_model()
            if model is None:
                self.firewall.logger.error(
                    "Nenhum modelo de IA carregado",
                    service="AIAnalyzer",
                    suggestion="Selecionar modelo válido"
                )
                return None
            
            # Faz predição
            prediction = model.predict(df)
            probability = model.predict_proba(df)
            
            # Calcula score baseado na probabilidade
            max_prob = np.max(probability[0])
            score = int(max_prob * 100)
            
            if score >= 70:  # Limiar para considerar como ameaça
                # Log da detecção
                self.firewall.logger.attack(
                    "Ameaça detectada por IA",
                    ip=features.get('src_ip'),
                    port=features.get('dst_port'),
                    service="AI Analysis",
                    suggestion="Investigar tráfego",
                    additional_data={
                        'prediction': int(prediction[0]),
                        'confidence': float(max_prob),
                        'features': features
                    }
                )
                
                return {
                    'block': score >= 85,
                    'reason': f"Modelo de IA detectou ameaça (classe {prediction[0]}, confiança {max_prob:.2f})",
                    'score': score,
                    'details': {
                        'ai_prediction': int(prediction[0]),
                        'confidence': float(max_prob),
                        'features': features
                    }
                }
                
        except Exception as e:
            self.firewall.logger.error(
                "Erro na análise por IA",
                service="AIAnalyzer",
                suggestion="Verificar dados de entrada",
                additional_data={'error': str(e)}
            )
            
        return None
    
    def analyze_traffic(self):
        """Análise em lote do tráfego acumulado"""
        model = self.ai_chooser.get_current_model()
        if not model:
            self.ai_chooser.log_event("Nenhum modelo carregado.", error=True)
            return

        df = self.extractor.get_feature_dataframe()

        if df.empty:
            self.ai_chooser.log_event("Nenhum dado de tráfego disponível para análise.")
            return

        try:
            # Converte para float64 se necessário
            df = df.astype('float64')

            predictions = model.predict(df)

            for idx, pred in enumerate(predictions):
                if pred != 0:
                    ip = df.iloc[idx].get("src_ip", "IP_DESCONHECIDO")
                    classe = str(pred)

                    self.ai_chooser.log_event(f"⚠️ Alerta: Padrão suspeito detectado no fluxo #{idx} (Classe: {classe}, IP: {ip})")

                    if self.firewall.acl_manager and ip != "IP_DESCONHECIDO":
                        success = self.firewall.acl_manager.block_ip(
                            ip=ip,
                            reason=f"Ataque Classe {classe}",
                            source="AIAnalyzer"
                        )
                        if success:
                            self.ai_chooser.log_event(f"IP {ip} bloqueado com sucesso.")
                        else:
                            self.ai_chooser.log_event(f"Falha ao bloquear IP {ip}.", error=True)

        except Exception as e:
            self.ai_chooser.log_event(f"Erro durante análise de tráfego: {e}", error=True)

        self.extractor.reset()

    def test_ai_analysis(self, features):
        """Método para testar a IA com features específicas"""
        if not self.model:
            print("❌ Modelo de IA não carregado!")
            return None

        try:
            df = pd.DataFrame([features])
            prediction = self.model.predict(df)
            proba = self.model.predict_proba(df)
            
            print("\n🔍 Resultado do Teste de IA:")
            print(f"📊 Features: {features}")
            print(f"🎯 Predição: {prediction[0]} (0=Normal, 1=Malicioso)")
            print(f"📈 Probabilidade: Normal={proba[0][0]:.2f}, Malicioso={proba[0][1]:.2f}")
            
            return prediction[0]
        except Exception as e:
            print(f"❌ Erro durante análise: {e}")
            return None

class AIChooser:
    """Seleciona e carrega o modelo de IA a ser utilizado"""
    
    def __init__(self, ui, model_paths=None):
        self.ui = ui
        self.model_paths = model_paths or {
            0: 'Models\\xgboost_model.model',
            1: 'Models\\random_forest_model.pkl'
        }
        self.model = None
        self.current_model_name = None

        # Conecta a UI à função de carregamento
        self.ui.comboBox_ModeloIA.currentIndexChanged.connect(self.load_selected_model)
        self.ui.comboBox_ModeloIA.setCurrentIndex(1)
        self.load_selected_model()
    
    def load_selected_model(self):
        """Carrega o modelo selecionado na UI"""

        if hasattr(self.ui, 'comboBox_ModoGamer'):
            if self.ui.comboBox_ModoGamer.currentIndex() == 0:  # Modo gamer ativado
                self.log_event("Modo Gamer ativado - Modelo de IA não será carregado")
                return None

        model_index = self.ui.comboBox_ModeloIA.currentIndex()

        if model_index not in self.model_paths:
            self.log_event(f"Índice de modelo '{model_index}' não encontrado.", error=True)
            return None

        model_path = self.model_paths[model_index]

        try:
            if model_path.endswith(".model"):
                import xgboost as xgb
                self.model = xgb.XGBClassifier()
                self.model.load_model(model_path)
            elif model_path.endswith(".pkl"):
                import joblib
                self.model = joblib.load(model_path)
            else:
                self.log_event(f"Formato de modelo não suportado: {model_path}", error=True)
                return None

            self.current_model_name = model_path
            self.log_event(f"Modelo '{model_path}' carregado com sucesso.")
            return self.model
            
        except Exception as e:
            self.log_event(f"Erro ao carregar modelo '{model_path}': {e}", error=True)
            return None

    def get_current_model(self):
        """Retorna o modelo atualmente carregado"""
        return self.model
    
    def log_event(self, message, error=False):
        """Registra eventos e mostra na UI"""
        prefix = "[ERRO]" if error else "[INFO]"
        print(f"{prefix} {message}")
        if error:
            QMessageBox.critical(None, "Erro", message)
        else:
            QMessageBox.information(None, "Info", message)

class ACLManager:
    """Gerenciador de ACL (Access Control List) para bloquear IPs maliciosos"""
    
    def __init__(self):
        self.blocked_ips = set()
        self.lock = threading.Lock()
        self.acl_logfile = "acl_block.log"
        
        # Inicializa o arquivo de log se não existir
        if not os.path.exists(self.acl_logfile):
            with open(self.acl_logfile, 'w') as f:
                f.write("ACL Block Log\n")
                f.write("="*50 + "\n")
    
    def block_ip(self, ip, reason, source):
        """Bloqueia um IP adicionando uma regra de firewall"""
        with self.lock:
            if ip in self.blocked_ips:
                return False  # IP já está bloqueado
                
            try:
                # Formata o motivo para ser usado no nome da regra
                clean_reason = re.sub(r'[^a-zA-Z0-9_]', '_', reason)[:50]
                clean_source = re.sub(r'[^a-zA-Z0-9_]', '_', source)[:20]
                
                # Comando para Windows (netsh)
                if platform.system() == 'Windows':
                    rule_name = f"BLOCK_{clean_source}_{clean_reason}_{ip}"
                    cmd = (
                        f"netsh advfirewall firewall add rule "
                        f"name=\"{rule_name}\" "
                        f"dir=in action=block remoteip={ip} "
                        f"enable=yes"
                    )
                    
                    # Executa o comando
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    
                    if result.returncode == 0:
                        self.blocked_ips.add(ip)
                        self._log_block(ip, reason, source)
                        return True
                    else:
                        return False
                
                # Comando para Linux (iptables)
                elif platform.system() == 'Linux':
                    cmd = f"iptables -A INPUT -s {ip} -j DROP"
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    
                    if result.returncode == 0:
                        self.blocked_ips.add(ip)
                        self._log_block(ip, reason, source)
                        return True
                    else:
                        return False
                
                else:
                    return False
                    
            except subprocess.CalledProcessError as e:
                return False
            except Exception as e:
                return False
    
    def _log_block(self, ip, reason, source):
        """Registra o bloqueio no arquivo de log"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "ip": ip,
            "reason": reason,
            "source": source,
            "action": "blocked"
        }
        
        try:
            with open(self.acl_logfile, 'a') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Erro ao registrar bloqueio no log: {str(e)}")
    
    def is_blocked(self, ip):
        """Verifica se um IP está bloqueado"""
        with self.lock:
            return ip in self.blocked_ips

class WindowsInterfaceManager:

    @staticmethod
    def get_active_interface():
        try:
            interfaces = []
            for name, addrs in psutil.net_if_addrs().items():
                # Filtra apenas interfaces físicas principais
                if not name.startswith(('Wi-Fi', 'Ethernet', 'Local Area Connection')):
                    continue
                # Verifica se tem endereço IPv4 (family=2)
                if any(addr.family == 2 for addr in addrs):
                    interfaces.append(name)
            
            # Prioriza Ethernet sobre Wi-Fi se ambas existirem
            if interfaces:
                ethernet = next(
                    (iface for iface in interfaces 
                     if 'Ethernet' in iface or 'Local Area Connection' in iface), 
                    None
                )
                return ethernet if ethernet else interfaces[0]
            return None
            
        except Exception as e:
            print(f"[!] Erro ao detectar interfaces: {str(e)}")
            return None

class JA3DatabaseManager:
    def __init__(self):
        self.ja3_bloom = ScalableBloomFilter(
            initial_capacity=10000, 
            error_rate=0.001
        )
        self.last_update = None
        self.update_interval = timedelta(hours=24)
        self.lock = threading.Lock()
        
        # Fontes alternativas confiáveis
        self.data_sources = [
            self._fetch_sslblacklist,
            self._fetch_emergingthreats
        ]
        
        self._update_database()

    def _fetch_sslblacklist(self):
        #Def responsável por buscar fingerprints da JA3
        try:
            url = "https://sslbl.abuse.ch/downloads/ja3_fingerprints.csv"
            response = requests.get(url, timeout=15)
            return [
                line.split(",")[0] 
                for line in response.text.splitlines() 
                if line and not line.startswith("#")
            ]
        except Exception as e:
            print(f"[JA3] Erro SSL Blacklist: {str(e)}")
            return []

    def _fetch_emergingthreats(self):
        #Def responsável por buscar fingerprints da JA3
        """Fonte secundária: Emerging Threats"""
        try:
            url = "https://rules.emergingthreats.net/blockrules/ja3-fingerprints.txt"
            response = requests.get(url, timeout=15)
            return [
                line.strip() 
                for line in response.text.splitlines() 
                if line and not line.startswith("#")
            ]
        except Exception as e:
            print(f"[JA3] Erro Emerging Threats: {str(e)}")
            return []

    def _update_database(self):
        #Def para atualiar o vanco de dados de fingerprints JA3 
        new_hashes = set()
        
        for source in self.data_sources:
            try:
                hashes = source()
                new_hashes.update(hashes)
                print(f"[JA3] {len(hashes)} hashes de {source.__name__}")
            except Exception as e:
                print(f"[JA3] Erro em {source.__name__}: {str(e)}")
        
        if not new_hashes:
            print("[JA3] AVISO: Nenhum hash válido obtido das fontes!")
            return
            
        with self.lock:
            # CORREÇÃO: Usar initial_capacity em vez de capacity
            self.ja3_bloom = ScalableBloomFilter(
                initial_capacity=max(len(new_hashes)*2, 10000),  # Corrigido aqui
                error_rate=0.001
            )
            
            for ja3_hash in new_hashes:
                if ja3_hash and len(ja3_hash) == 32:  # Valida formato MD5
                    self.ja3_bloom.add(ja3_hash)
            
            self.last_update = datetime.now()
            print(f"[JA3] Database atualizada. Hashes únicos: {len(new_hashes)}")

    def start_auto_update(self):
        #Implementa um mecanismo de atualização automática para o banco de dados JA3.
        def updater():
            while True:
                try:
                    now = datetime.now()
                    if not self.last_update or (now - self.last_update) >= self.update_interval:
                        print("[JA3] Iniciando atualização periódica...")
                        self._update_database()
                except Exception as e:
                    print(f"[JA3] Erro no updater: {str(e)}")
                
                time.sleep(60)  # Verifica a cada minuto

        threading.Thread(target=updater, daemon=True).start()

    def is_malicious(self, ja3_hash):
        #Verifica se os hashs são maliciosos
        if not ja3_hash or len(ja3_hash) != 32:
            return False
            
        with self.lock:
            if ja3_hash in self.ja3_bloom:  # Verificação rápida
                return self._double_check(ja3_hash)  # Confirmação
        return False
        
    def _double_check(self, ja3_hash):
        """Verificação secundária contra uma fonte mais precisa"""
        # Exemplo: consultar um banco de dados exato (não probabilístico)
        return ja3_hash in self.exact_database  # Supondo que existe uma lista exata

class AdvancedFirewall(QObject):
    alert_triggered = Signal(str)
    _instance = None  # Controle de instância única

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, ui=None, log_file="firewall_logs.json"):
        if hasattr(self, '_initialized'):  # Evita reinicialização
            return
            
        super().__init__()
        self._initialized = True  # Marca como inicializado
        
        # Configurações básicas
        self.ui = ui
        self.logger = JSONLogger(log_file)  # Novo logger JSON
        self.running = False
        self.gamer_mode = False
        
        # Componentes principais (inicializados uma única vez)
        self._initialize_components()

    def set_gamer_mode(self, enabled):
        """Ativa/desativa o modo gamer"""
        self.gamer_mode = enabled
        if enabled:
            # Remove o analisador de IA da pipeline se existir
            if hasattr(self.pipeline, 'steps') and self.ai_analyzer in self.pipeline.steps:
                self.pipeline.steps.remove(self.ai_analyzer)
            self.logger.info(
                "Modo Gamer ativado",
                service="Firewall Core",
                suggestion="IA desativada para performance"
            )
        else:
            # Adiciona o analisador de IA de volta se estiver disponível
            if hasattr(self, 'ai_analyzer') and self.ai_analyzer and self.ai_analyzer not in self.pipeline.steps:
                self.pipeline.steps.append(self.ai_analyzer.analyze)
            self.logger.info(
                "Modo Gamer desativado",
                service="Firewall Core",
                suggestion="IA reativada para análise"
            )
    
    def _initialize_components(self):
        """Inicializa todos os componentes do firewall uma única vez"""
        # Gerenciadores
        self.acl_manager = ACLManager()
        self.ja3_db = JA3DatabaseManager()
        
        # Sistema de IA (opcional)
        self.ai_chooser = AIChooser(self.ui) if self.ui else None
        
        # Pipeline de análise
        self.pipeline = AnalysisPipeline(self)
        
        # Estatísticas e cache
        self._init_statistics()
        self._init_network_interface()
        
    def _init_statistics(self):
        """Inicializa estruturas para coleta de estatísticas"""
        self.stats = {
            'packets_processed': 0,
            'ja3_matches': 0,
            'yara_matches': 0,
            'dpi_alerts': 0,
            'ips_blocked': 0,
            'last_alert': None,
            'ai_detections': 0
        }
        
        self.flow_cache = {}
        self.ddos_stats = {}
        self.flow_lock = threading.Lock()
        self.ddos_thresholds = {
            'packet_rate': 1000,
            'bandwidth': 10e6,
            'syn_rate': 500
        }

    def _init_network_interface(self):
        """Configura a interface de rede"""
        self.interface = WindowsInterfaceManager.get_active_interface()
        if not self.interface:
            available = get_if_list()
            self.logger.error(
                "Nenhuma interface de rede ativa encontrada",
                service="Network",
                suggestion="Verificar conexão de rede",
                additional_data={'interfaces_disponiveis': available}
            )
            raise RuntimeError(
                f"Nenhuma interface de rede ativa encontrada!\n"
                f"Interfaces disponíveis: {', '.join(available)}"
            )
        self.logger.info(
            "Interface de rede selecionada",
            service="Network",
            additional_data={'interface': self.interface}
        )

    def _process_packet(self, pkt):
        """Método modificado para usar o pipeline"""
        self.stats['packets_processed'] += 1
        
        if not pkt.haslayer(IP):
            return

        try:
            # Processa o pacote através do pipeline
            result = self.pipeline.process_packet(pkt)
            
            if result['block']:
                src_ip = pkt[IP].src
                self._block_ip(src_ip, result['reason'])
                
        except Exception as e:
            self.logger.error(
                "Erro ao processar pacote",
                service="Firewall Core",
                suggestion="Verificar pipeline de análise",
                additional_data={'error': str(e)}
            )

    def _init_metadata_analyzer(self):
        #Inicia o sistema de análise de metadados do firewall, criando uma estrutura para rastrear e analisar padrões de conexão suspeitos.
        self.connections = defaultdict(lambda: {'count': 0, 'ports': set(), 'ja3': set()})

    def start(self):
        #Inicia o firewall
        self.logger.info(
            "Iniciando firewall avançado",
            service="Firewall Core",
            additional_data={
                'interface': self.interface,
                'gamer_mode': self.gamer_mode
            }
        )
        
        self.running = True
        try:
            self.sniff_thread = threading.Thread(
                target=self._start_sniffing,
                daemon=True
            )
            self.sniff_thread.start()
            
            self._control_interface()
            
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            self.logger.error(
                "Erro ao iniciar firewall",
                service="Firewall Core",
                suggestion="Verificar permissões e configuração",
                additional_data={'error': str(e)}
            )
            self.stop()

    def _start_sniffing(self):
        #inicia a inspeção de pacotes
        self.logger.info(
            "Iniciando captura de pacotes",
            service="Network",
            additional_data={'interface': self.interface}
        )
        
        sniff(
            iface=self.interface,
            prn=self._process_packet,
            filter="tcp or udp",
            store=False
        )

    def stop(self):
        #Para o firewall
        self.logger.info(
            "Parando firewall",
            service="Firewall Core",
            additional_data={'stats': self.stats}
        )
        
        self.running = False
        if hasattr(self, 'sniff_thread'):
            self.sniff_thread.join(timeout=1)

    def _log_tls_anomaly(self, pkt):
        #Registra anomalias TLS para análise posterior
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'source_ip': pkt[IP].src if pkt.haslayer(IP) else None,
            'destination_ip': pkt[IP].dst if pkt.haslayer(IP) else None,
            'anomaly_type': 'Non-standard TLS cipher',
            'details': 'anomaly',
            'packet_summary': pkt.summary()
        }
        
        try:
            with open('tls_anomalies.log', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            self.logger.error(
                "Falha ao registrar anomalia TLS",
                service="TLS Inspection",
                suggestion="Verificar permissões de arquivo",
                additional_data={'error': str(e)}
            )

    def _block_ip(self, ip, reason):
        """Método modificado para usar o ACLManager"""
        # Verifica se o IP já está bloqueado
        if self.acl_manager.is_blocked(ip):
            return False
            
        # Usa o ACLManager para bloquear o IP
        success = self.acl_manager.block_ip(ip, reason, "FirewallCore")
        
        if success:
            with self.flow_lock:
                self.stats['ips_blocked'] += 1
                self.logger.info(
                    "IP bloqueado com sucesso",
                    ip=ip,
                    service="ACL",
                    suggestion="Monitorar atividade",
                    additional_data={'reason': reason}
                )
                self.alert_triggered.emit(f"IP bloqueado: {ip} - Motivo: {reason}")
                
        return success

    def _control_interface(self):
        #Interface simples de controle
        while self.running:
            cmd = input("\nComando [stop/stats]: ").strip().lower()
            if cmd == "stop":
                self.stop()
                break
            elif cmd == "stats":
                print(json.dumps(self.stats, indent=2))
            else:
                print("Comando inválido")

def testar_firewall():
    """Função para testar os módulos manualmente"""
    print("\n🔍 Iniciando testes...")
    
    # Cria um firewall em modo de teste
    fw = AdvancedFirewall()
    
    # (1) Teste YARA - SQL Injection
    pkt_sqli = IP(src="10.0.0.1")/TCP(dport=80)/Raw(load="SELECT * FROM usuarios")
    resultado = fw.pipeline.yara_analyzer.analyze(pkt_sqli)
    print("\n🔎 Teste YARA (SQLi):", "✅ Bloqueado!" if resultado else "❌ Falhou!")
    
    # (2) Teste JA3 - Fingerprint malicioso
    pkt_tls = IP(src="192.168.1.100")/TLS()
    fw.ja3_db.is_malicious = lambda x: True  # Simula como malicioso
    resultado = fw.pipeline.ja3_analyzer.analyze(pkt_tls)
    print("🔎 Teste JA3 (TLS):", "✅ Bloqueado!" if resultado else "❌ Falhou!")
    
    # (3) Teste Estatístico - Portscan
    print("\n🔎 Simulando portscan...")
    for porta in range(80, 86):
        pkt = IP(src="192.168.1.50")/TCP(dport=porta)
        fw.pipeline.statistical_analyzer.analyze(pkt)
    print("Portscan detectado:", "✅" if len(fw.flow_cache) > 0 else "❌")

def testar_ia():
    """Testa o módulo de IA com dados simulados"""

    # Cria firewall em modo teste
    fw = AdvancedFirewall()
    
    if not fw.ai_chooser or not fw.ai_chooser.get_current_model():
        print("❌ Modelo de IA não está disponível!")
        return
    
    else:
        print("✅ Modelo de IA  disponível!")

    # Dados simulados (features extraídas de pacotes)
    casos_teste = [
        {"name": "Tráfego Normal", "features": {
            'flow_duration': 5.2, 'total_packets': 10, 'total_bytes': 1024,
            'mean_pkt_len': 100, 'std_pkt_len': 5, 'byte_rate': 200,
            'pkt_rate': 2, 'unique_flags': 3
        }},
        {"name": "Ataque DDoS", "features": {
            'flow_duration': 0.1, 'total_packets': 1000, 'total_bytes': 1000000,
            'mean_pkt_len': 1000, 'std_pkt_len': 150, 'byte_rate': 10000000,
            'pkt_rate': 10000, 'unique_flags': 1
        }}
    ]

    print("\n=== TESTE DO MÓDULO DE IA ===")
    for caso in casos_teste:
        print(f"\n🔎 Caso: {caso['name']}")
        resultado = fw.pipeline.ai_analyzer.test_ai_analysis(caso['features'])
        print("✅ Classificado corretamente!" if resultado == ("DDoS" in caso['name']) else "❌ Falha na classificação")

if __name__ == "__main__":
    if platform.system() != "Windows":
        print("[!] Este software é exclusivo para Windows!")
        sys.exit(1)
        
    try:
        # Cria uma única instância do firewall
        firewall = AdvancedFirewall()
        
        # Verifica se já está em execução
        if firewall.running:
            print("[!] O firewall já está em execução!")
            sys.exit(1)
            
        testar_firewall()
        
    except Exception as e:
        print(f"[!] Erro fatal: {str(e)}")
        sys.exit(1)