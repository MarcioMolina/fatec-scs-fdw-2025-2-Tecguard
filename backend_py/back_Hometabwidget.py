# main.py
import sys
import time
import random
import subprocess
import psutil
import pystray
from PIL import Image
import os
import json
import ctypes
import xgboost as xgb
import numpy as np
import tkinter as tk
import socket
import shutil
from datetime import timedelta
from tkinter import filedialog
from datetime import datetime
from win10toast import ToastNotifier
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QFileDialog, QMenu, QInputDialog, QLineEdit
from PySide6.QtCore import QTimer, Qt, QSharedMemory
from PySide6.QtGui import QColor, QAction
import win32com.client
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from back_firewall import AdvancedFirewall, AIChooser

caminho_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
caminho_imagens = os.path.join(caminho_base, "images")
caminho_interfaces = os.path.join(caminho_base, "interfaces")

sys.path.append(caminho_interfaces)



class NotificationManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.toaster = ToastNotifier()
        self.last_notification_time = 0
        self.notification_cooldown = 60  # Segundos entre notificações do mesmo tipo
        
    def load_config(self):
        """Carrega as configurações de notificação"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("notifications", True)
        except Exception:
            return True  # Padrão: notificações ligadas
        return True
    
    def save_config(self, enabled):
        """Salva o estado das notificações no arquivo de configuração"""
        try:
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            
            config["notifications"] = enabled
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")

    def show_notification(self, title, message, icon_path=None, duration=10):
        """Exibe uma notificação do Windows"""
        if not self.load_config():
            return  # Notificações desativadas
            
        # Verifica cooldown para evitar notificações em excesso
        current_time = time.time()
        if current_time - self.last_notification_time < self.notification_cooldown:
            return
            
        try:
            self.toaster.show_toast(
                title,
                message,
                icon_path=icon_path,
                duration=duration,
                threaded=True
            )
            self.last_notification_time = current_time
        except Exception as e:
            print(f"Erro ao exibir notificação: {e}")

    def get_icon_path(self, alert_type):
        """Retorna o caminho do ícone baseado no tipo de alerta"""
        icon_map = {
            "ataque": "alert_red.ico",
            "alerta": "alert_orange.ico",
            "suspeito": "alert_yellow.ico",
            "erro": "alert_purple.ico"
        }
        icon_name = icon_map.get(alert_type.lower(), "alert.ico")
        return os.path.join(caminho_imagens, icon_name)
    
class LogManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.log_file = "firewall_logs.json"
        
    def load_config(self):
        """Carrega as configurações de log"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("log_settings", {
                        "retention_days": 7,
                        "send_logs": False,
                        "log_server_ip": "",
                        "log_server_port": "514"
                    })
        except Exception:
            return {
                "retention_days": 7,
                "send_logs": False,
                "log_server_ip": "",
                "log_server_port": "514"
            }
    
    def save_config(self, settings):
        """Salva as configurações de log"""
        try:
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            
            config["log_settings"] = settings
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações de log: {e}")
    
    def cleanup_old_logs(self):
        """Remove logs mais antigos que o período de retenção configurado"""
        try:
            settings = self.load_config()
            retention_days = settings.get("retention_days", 7)
            
            if not os.path.exists(self.log_file):
                return
                
            # Lê todos os logs
            with open(self.log_file, 'r') as f:
                logs = [json.loads(line) for line in f if line.strip()]
            
            # Filtra logs dentro do período de retenção
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            filtered_logs = []
            
            for log in logs:
                try:
                    log_date = datetime.fromisoformat(log.get("timestamp", ""))
                    if log_date >= cutoff_date:
                        filtered_logs.append(log)
                except:
                    continue
            
            # Reescreve o arquivo apenas com logs válidos
            with open(self.log_file, 'w') as f:
                for log in filtered_logs:
                    f.write(json.dumps(log) + '\n')
            
            return len(logs) - len(filtered_logs)
            
        except Exception as e:
            print(f"Erro ao limpar logs antigos: {e}")
            return 0
    
    def send_logs_to_server(self, log_entry):
        """Envia logs para servidor remoto (syslog)"""
        try:
            settings = self.load_config()
            
            if not settings.get("send_logs", False):
                return False
                
            server_ip = settings.get("log_server_ip", "")
            server_port = settings.get("log_server_port", "514")
            
            if not server_ip:
                return False
            
            # Formata mensagem no formato syslog
            timestamp = log_entry.get("timestamp", datetime.now().isoformat())
            classification = log_entry.get("classification", "UNKNOWN")
            event = log_entry.get("event", "Unknown Event")
            ip = log_entry.get("ip", "N/A")
            port = log_entry.get("port", "N/A")
            
            syslog_message = f"<14>{timestamp} TecGuard[{classification}]: {event} - IP: {ip}, Porta: {port}"
            
            # Envia via socket UDP (protocolo syslog padrão)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(syslog_message.encode('utf-8'), (server_ip, int(server_port)))
            sock.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar log para servidor: {e}")
            return False
    
    def get_log_stats(self):
        """Retorna estatísticas dos logs"""
        try:
            if not os.path.exists(self.log_file):
                return {
                    "total_logs": 0,
                    "oldest_log": None,
                    "newest_log": None,
                    "by_classification": {}
                }
                
            with open(self.log_file, 'r') as f:
                logs = [json.loads(line) for line in f if line.strip()]
            
            stats = {
                "total_logs": len(logs),
                "oldest_log": None,
                "newest_log": None,
                "by_classification": {}
            }
            
            if logs:
                # Ordena por timestamp
                logs_sorted = sorted(logs, key=lambda x: x.get("timestamp", ""))
                stats["oldest_log"] = logs_sorted[0].get("timestamp")
                stats["newest_log"] = logs_sorted[-1].get("timestamp")
                
                # Conta por classificação
                for log in logs:
                    classification = log.get("classification", "UNKNOWN")
                    stats["by_classification"][classification] = stats["by_classification"].get(classification, 0) + 1
            
            return stats
            
        except Exception as e:
            print(f"Erro ao obter estatísticas de log: {e}")
            return {
                "total_logs": 0,
                "oldest_log": None,
                "newest_log": None,
                "by_classification": {}
            }

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, callback, log_file):
        self.callback = callback
        self.log_file = log_file
        self.last_position = 0
        self.last_modified = 0
        
        # Verifica se o arquivo existe para pegar a posição inicial
        if os.path.exists(self.log_file):
            self.last_modified = os.path.getmtime(self.log_file)
            with open(self.log_file, 'r') as f:
                f.seek(0, 2)  # Vai para o final do arquivo
                self.last_position = f.tell()
        
    def on_modified(self, event):
        if event.src_path == self.log_file:
            current_modified = os.path.getmtime(self.log_file)
            if current_modified <= self.last_modified:
                return  # Ignora modificações antigas
                
            self.last_modified = current_modified
            
            with open(self.log_file, 'r') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
                
                for line in new_lines:
                    line = line.strip()
                    if line:
                        try:
                            log_entry = json.loads(line)
                            self.callback(log_entry)
                        except json.JSONDecodeError:
                            continue


class JSONLogger:
    """Logger personalizado que gera logs em formato JSON com estrutura padronizada"""
    
    def __init__(self, log_file="firewall_logs.json"):
        self.log_file = log_file
        # Cria o arquivo de log se não existir
        open(self.log_file, 'a').close()
    
    def _log(self, event_name, classification, 
             ip=None, port=None,
             service=None, suggestion=None,
             additional_data=None):
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

    def info(self, event_name, **kwargs):
        """Log informativo"""
        self._log(event_name, "Informativo", **kwargs)
    
    def error(self, event_name, **kwargs):
        """Log de erro"""
        self._log(event_name, "Erro", **kwargs)
    
    def warning(self, event_name, **kwargs):
        """Log de alerta"""
        self._log(event_name, "Alerta", **kwargs)
    
    def attack(self, event_name, **kwargs):
        """Log de ataque detectado"""
        self._log(event_name, "Ataque", **kwargs)
    
    def suspicious(self, event_name, **kwargs):
        """Log de atividade suspeita"""
        self._log(event_name, "Suspeito", **kwargs)

class FirewallApp(QMainWindow):
    def __init__(self):
        self.shared_mem = QSharedMemory("TecSec-Tecguard-Unique-Key")
        if not self.shared_mem.create(1):
            QMessageBox.warning(None, "Aviso", "O aplicativo já está em execução!")
            sys.exit(1)
        
        self.toaster = ToastNotifier()
        self.setup_log_monitor()

        super().__init__()

        self.config_file = "config.json"
        self.config = self.load_config()
        self.logger = JSONLogger("firewall_logs.json")  # Instância do logger
        self.notification_manager = NotificationManager(self.config_file)
        
        # Carrega a UI correta baseada no tema
        self.load_ui_based_on_theme()

        self.tray_icon = None  # Inicializa como None
        
        self.network_stats = {}
        self.old_upload = 0
        self.old_download = 0
        self.alert_count = 0
        
        # Configurações iniciais
        self.Choser = AIChooser(self.ui)
        self.setup_connections()
        self.setup_initial_data()
        self.setup_timers()
        self.setup_table()
        self.setup_connections()
        self.update_connections()
        self.setup_initial_data()
        self.setup_timers()
        self.log_manager = LogManager(self.config_file)
        self.setup_log_management()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(2000)
        self.timer.timeout.connect(self.update_network_stats)
        self.timer.timeout.connect(self.update_connections)
        self.ui.button_CriarACL.clicked.connect(self.criar_acl)
        self.ui.button_RemoverACL.clicked.connect(self.excluir_acl_por_nome)
        self.ui.tableWidget.cellClicked.connect(self.preparar_edicao)
        self.ui.pushButton_relatorio.clicked.connect(self.generate_report)
        self.ui.tabHome.currentChanged.connect(self.on_tab_changed)
        self.ui.tableWidget_relatorio.customContextMenuRequested.connect(self.show_table_context_menu)
        self.ui.button_ImportarACL.clicked.connect(self.importar_ACL)
        self.ui.comboBox_PopupdeNotif.currentIndexChanged.connect(self.toggle_notifications)
        # Carrega a preferência de notificações
        self.notifications_enabled = self.config.get("notifications", True)
        
        # Configura o combobox conforme o valor carregado
        self.ui.comboBox_PopupdeNotif.setCurrentIndex(0 if self.notifications_enabled else 1)
        
        current_theme = self.config.get("theme", "dark")
        self.ui.comboBox_Tema.setCurrentIndex(1 if current_theme == "dark" else 0)

        self.tray_icon = None
        self.setup_tray_icon()

        # Inicializa o firewall
        self.firewall = AdvancedFirewall()
        self.firewall_thread = None
        self.init_firewall()

    def setup_log_monitor(self):
        """Configura o monitoramento do arquivo de log"""
        log_file = "firewall_logs.json"
        
        # Cria o arquivo se não existir
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.write("")
        
        self.log_observer = Observer()
        event_handler = LogFileHandler(self.check_for_alerts, log_file)
        self.log_observer.schedule(event_handler, path='.', recursive=False)
        self.log_observer.start()
        
    def check_for_alerts(self):
        """Verifica se há alertas nos logs e atualiza a interface"""
        try:
            # Verifica se o arquivo de logs existe
            if not os.path.exists("firewall_logs.json"):
                self.set_no_alerts()
                return
                
            # Lê o arquivo de logs
            with open("firewall_logs.json", "r") as f:
                logs = [json.loads(line) for line in f if line.strip()]
                
            # Procura por alertas recentes (últimas 24 horas)
            now = datetime.now()
            has_alerts = False
            latest_alert = None
            
            for log in logs:
                try:
                    log_time = datetime.fromisoformat(log.get("timestamp", ""))
                    if (now - log_time).total_seconds() > 86400:  # 24 horas
                        continue
                        
                    if log.get("classification", "").lower() in ["ataque", "alerta", "suspeito"]:
                        has_alerts = True
                        latest_alert = log
                        break
                except:
                    continue
                    
            if has_alerts and latest_alert:
                self.set_alert_status(
                    alert=True,
                    title="ALERTA DE SEGURANÇA",
                    message=f"{latest_alert.get('event', 'Evento desconhecido')}\n"
                            f"IP: {latest_alert.get('ip', 'Desconhecido')}\n"
                            f"Porta: {latest_alert.get('port', 'N/A')}"
                )
            else:
                self.set_no_alerts()
                
        except Exception as e:
            self.logger.error("Erro ao verificar alertas", error=str(e))
            self.set_no_alerts()

    def set_alert_status(self, alert, title=None, message=None):
        """Define o estado do alerta na interface"""
        if alert:
            # Configuração para quando há alerta
            self.ui.label_Alerta.setStyleSheet("font: 24pt 'Segoe UI'; color: red;")
            self.ui.label_Alerta.setText("ALERTA!")
            
            self.ui.label_Alertanotif.setStyleSheet("font: 35pt 'Segoe UI'; color: red;")
            self.ui.label_Alertanotif.setText(message if message else "Ataque detectado!")
        else:
            # Configuração para quando não há alertas
            self.set_no_alerts()

    def set_no_alerts(self):
        """Define o estado sem alertas na interface"""
        self.ui.label_Alerta.setStyleSheet("font: 24pt 'Segoe UI'; color: green;")
        self.ui.label_Alerta.setText("SEM ALERTAS")
        
        self.ui.label_Alertanotif.setStyleSheet("font: 20pt 'Segoe UI'; color: white;")
        self.ui.label_Alertanotif.setText("Nenhuma atividade suspeita detectada")
                
    def show_attack_notification(self, log_data):
        """Exibe notificação do Windows para eventos importantes"""
        try:
            # Configuração da notificação
            title = "⚠️ "
            if log_data['classification'].lower() == 'ataque':
                title += "Ataque Detectado!"
            elif log_data['classification'].lower() == 'alerta':
                title += "Alerta de Segurança"
            else:
                title += "Atividade Suspeita"
            
            message = (
                f"Evento: {log_data.get('event', 'Evento desconhecido')}\n"
                f"Origem: {log_data.get('ip', 'IP desconhecido')}\n"
                f"Porta: {log_data.get('port', 'N/A')}"
            )
            
            # Ícone - substitua pelo caminho do seu ícone
            icon_path = os.path.join(caminho_imagens, "alert.ico")
            
            # Exibe a notificação
            self.toaster.show_toast(
                title,
                message,
                icon_path=icon_path if os.path.exists(icon_path) else None,
                duration=10,
                threaded=True
            )
            
        except Exception as e:
            self.logger.error("Falha na notificação", error=str(e))
            
    def closeEvent(self, event):
        """Garante que o observer seja encerrado corretamente"""
        if hasattr(self, 'log_observer'):
            self.log_observer.stop()
            self.log_observer.join()
        super().closeEvent(event)
    
    
    def init_firewall(self):
        """Inicializa o firewall corretamente"""
        try:
            from back_firewall import AdvancedFirewall  # Import aqui para evitar circular imports
            self.firewall = AdvancedFirewall()
            
            # Verificação adicional
            if not hasattr(self.firewall, 'alert_triggered'):
                raise AttributeError("Firewall não possui o signal alert_triggered")
                
            self.logger.info("Firewall inicializado com sucesso", service="Firewall")
            return True
            
        except Exception as e:
            self.logger.error("Falha ao inicializar firewall", service="Firewall", error=str(e))
            self.firewall = None
            return False
    
    def load_ui_based_on_theme(self):
        """Carrega o arquivo UI baseado em tema e resolução"""
        theme = self.config.get("theme", "dark")
        resolution = self.config.get("resolution", "hd")  # Padrão para FHD
        
        # Remove a UI atual se já existir
        if hasattr(self, 'ui'):
            self.ui.centralwidget.setParent(None)
            del self.ui

        # Mapeia para nome do módulo
        nome_arquivo = f"Hometabwidget_{theme}_{resolution}"
        
        try:
            # Importa dinamicamente o módulo correto
            module = __import__(nome_arquivo)
            self.ui = module.Ui_MainWindow()
            self.ui.setupUi(self)
            
            # Reconecta todos os sinais
            self.setup_connections()
            
            # Restaura o estado da interface
            self.restore_interface_state()
            
        except ImportError as e:
            self.logger.error(f"Falha ao carregar interface {nome_arquivo}", service="UI", error=str(e))
            QMessageBox.critical(self, "Erro", 
                f"Falha ao carregar interface {nome_arquivo}:\n{str(e)}\n"
                f"Carregando interface padrão...")
            
            # Fallback para FHD escuro
            module = __import__("Hometabwidget_dark_hd")
            self.ui = module.Ui_MainWindow()
            self.ui.setupUi(self)
            self.setup_connections()

    def restore_interface_state(self):
        """Restaura o estado da interface após troca de tema/resolução"""
        # Restaura o combobox para o tema atual
        current_theme = self.config.get("theme", "dark")
        self.ui.comboBox_Tema.setCurrentIndex(1 if current_theme == "dark" else 0)
        
        # Restaura o combobox para a resolução atual
        current_resolution = self.config.get("resolution", "hd")
        resolution_map = {"hd": 0, "fhd": 1, "small": 2}
        self.ui.comboBox_Resolucao.setCurrentIndex(resolution_map.get(current_resolution, 0))

    def change_theme(self, index):
        """Altera o tema da aplicação baseado no combobox"""
        theme_map = {
            0: "white",
            1: "dark"
        }
        
        selected_theme = theme_map.get(index, "dark")
        
        if selected_theme != self.config.get("theme", "dark"):
            self.logger.info(
                "Tema alterado",
                service="UI Configuration",
                additional_data={
                    "old_theme": self.config.get("theme", "dark"),
                    "new_theme": selected_theme
                }
            )
            
            self.config["theme"] = selected_theme
            self.save_config()
            
            msg = QMessageBox()
            msg.setWindowTitle("Reiniciar aplicativo")
            msg.setText("O tema será aplicado após reiniciar o aplicativo.")
            msg.setInformativeText("Deseja reiniciar agora?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            
            resposta = msg.exec()
            
            if resposta == QMessageBox.Yes:
                self.restart_application()
            else:
                current_theme = self.config.get("theme", "dark")
                self.ui.comboBox_Tema.setCurrentIndex(1 if current_theme == "dark" else 0)

    def restart_application(self):
        """Reinicia o aplicativo mantendo os argumentos"""
        self.logger.info("Reiniciando aplicação", service="Application Lifecycle")
        QApplication.quit()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def load_config(self):
        """Carrega as configurações do arquivo ou cria um padrão"""
        default_config = {
            "theme": "dark",
            "window_size": "hd",
            "notifications": "true",
            "window_position": [100, 100]
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error("Erro ao carregar configurações", service="Configuration", error=str(e))
        
        return default_config
    
    def toggle_notifications(self, index):
        """Ativa/desativa notificações conforme combobox"""
        # 0 = Ligado, 1 = Desligado (conforme itens do combobox)
        notifications_enabled = (index == 0)
        
        # Atualiza o gerenciador de notificações
        self.notification_manager.save_config(notifications_enabled)
        
        # Atualiza o JSON de configurações
        self.config["notifications"] = notifications_enabled
        self.save_config()
        
        status = "ativadas" if notifications_enabled else "desativadas"
        self.logger.info(f"Notificações {status}", service="Configuration")
        
        # Mostra feedback visual
        if notifications_enabled:
            QMessageBox.information(self, "Notificações", "Notificações ativadas com sucesso!")
        else:
            QMessageBox.information(self, "Notificações", "Notificações desativadas.")

            
    def show_alert_notification(self, log_data):
        """Exibe notificação do Windows para eventos importantes"""
        classification = log_data.get('classification', '').lower()
        
        # Configuração da notificação baseada no tipo de alerta
        if classification == 'ataque':
            title = "⚠️ Ataque Detectado!"
            icon = self.notification_manager.get_icon_path("ataque")
        elif classification == 'alerta':
            title = "⚠️ Alerta de Segurança"
            icon = self.notification_manager.get_icon_path("alerta")
        elif classification == 'suspeito':
            title = "⚠️ Atividade Suspeita"
            icon = self.notification_manager.get_icon_path("suspeito")
        else:  # erro
            title = "⚠️ Erro no Sistema"
            icon = self.notification_manager.get_icon_path("erro")
        
        # Mensagem detalhada
        message = (
            f"Evento: {log_data.get('event', 'Evento desconhecido')}\n"
            f"Origem: {log_data.get('ip', 'IP desconhecido')}\n"
            f"Porta: {log_data.get('port', 'N/A')}"
        )
        
        # Exibe a notificação
        self.notification_manager.show_notification(title, message, icon)
        
        # Adiciona também na interface (opcional)
        self.ui.label_Alertanotif.setText(f"{title}: {message}")
        self.ui.label_Alertanotif.setStyleSheet("color: red;")
        QTimer.singleShot(5000, lambda: self.ui.label_Alertanotif.setStyleSheet("color: white;"))

    def save_config(self):
        """Salva as configurações atuais no arquivo"""
        try:
            self.config["notifications"] = self.notifications_enabled

            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            self.logger.error("Erro ao salvar configurações", service="Configuration", error=str(e))
        
    def setup_tray_icon(self):
        """Configura o ícone na área de notificação"""
        try:
            icon_path = os.path.join(caminho_imagens, "interneticone.png")
            image = Image.open(icon_path)
            
            menu = pystray.Menu(
                pystray.MenuItem('Abrir', self.show_window),
                pystray.MenuItem('Sair', self.quit_app)
            )
            
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.stop()
                
            self.tray_icon = pystray.Icon(
                "TecSec-Tecguard",
                image,
                "TecSec-Tecguard",
                menu
            )
            
            self.tray_icon.run_detached()
            self.logger.info("Ícone da bandeja configurado", service="UI")
            
        except Exception as e:
            self.logger.error("Erro ao criar ícone da bandeja", service="UI", error=str(e))
            QApplication.quit()

    def closeEvent(self, event):
        """Override do método de fechar janela"""
        self.config["window_size"] = [self.width(), self.height()]
        self.config["window_position"] = [self.x(), self.y()]
        self.save_config()

        self.setup_tray_icon()
        event.ignore()
        self.hide()
        
        if self.tray_icon:
            self.tray_icon.notify(
                "O aplicativo continua em execução", 
                "Clique no ícone para restaurar a janela."
            )
            
    def show_window(self):
        """Restaura a janela principal"""
        self.showNormal()
        self.activateWindow()
        
    def quit_app(self):
        """Fecha o aplicativo completamente"""
        self.logger.info("Aplicativo sendo encerrado", service="Application Lifecycle")
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.stop()
        QApplication.quit()
    
    def setup_initial_data(self):
        """Preenche as tabelas com dados iniciais"""
        self.update_table()
        self.populate_acls_table()
        self.populate_reports_table()
        self.populate_acls_table2()

    def handle_firewall_alert(self, message):
        """Exibe alertas do firewall na interface"""
        self.ui.label_Alertanotif.setText(message)
        self.ui.label_Alertanotif.setStyleSheet("color: red;")
        
        row = self.ui.tableWidget_relatorio.rowCount()
        self.ui.tableWidget_relatorio.insertRow(row)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.tableWidget_relatorio.setItem(row, 0, QTableWidgetItem(timestamp))
        self.ui.tableWidget_relatorio.setItem(row, 1, QTableWidgetItem("Alerta de Firewall"))
        self.ui.tableWidget_relatorio.setItem(row, 2, QTableWidgetItem(message))

    def update_network_stats(self):
        try:
            net_io = psutil.net_io_counters()
            current_upload = net_io.bytes_sent
            current_download = net_io.bytes_recv
            
            upload_diff = (current_upload - self.old_upload) / 1024
            download_diff = (current_download - self.old_download) / 1024

            if upload_diff >= 1024.0:
                upload_mbs = upload_diff/1024
                self.ui.label_Upload.setText(f"{upload_mbs:.1f} MB/s")
            else:
                self.ui.label_Upload.setText(f"{upload_diff:.1f} KB/s")
            if download_diff > 1024.0:
                download_mbs = download_diff/1024
                self.ui.label_Download.setText(f"{download_mbs:.1f} MB/s")
            else:
                self.ui.label_Download.setText(f"{download_diff:.1f} KB/s")
            
            self.check_network_activity(upload_diff, download_diff)
            
            self.old_upload = current_upload
            self.old_download = current_download

        except Exception as e:
            self.logger.error("Erro ao atualizar estatísticas de rede", service="Network", error=str(e))

    def update_connections(self):
        """Atualiza o número de conexões estabelecidas"""
        connections = psutil.net_connections(kind='inet')
        established = len([conn for conn in connections if conn.status == 'ESTABLISHED'])
        self.ui.label_CoEstabelecidas.setText(f"{established} Conexões estabelecidas")
        
        if established > 100 and self.alert_count < 3:
            self.trigger_alert(f"Muitas conexões ativas: {established}")
                  
    def check_network_activity(self, upload, download):
        """Verifica atividade suspeita na rede"""
        threshold = 500
        if upload > threshold or download > threshold:
            direction = "upload" if upload > threshold else "download"
            self.trigger_alert(f"Alta atividade de {direction}: {max(upload, download):.1f} KB/s")
    
    def trigger_alert(self, message):
        """Dispara um alerta na interface"""
        self.alert_count += 1
        self.ui.label_Alertanotif.setText(f"{self.alert_count} Alerta(s): {message}")
        self.ui.label_Alertanotif.setStyleSheet("font: 20pt \"Segoe UI\"; color: red;")
        QTimer.singleShot(3000, lambda: self.ui.label_Alertanotif.setStyleSheet("font: 20pt \"Segoe UI\"; color: white;"))

    def setup_timers(self):
        """Configura timers para atualização dinâmica"""
        self.alerts_timer = QTimer(self)
        self.alerts_timer.timeout.connect(self.check_for_alerts)
        self.alerts_timer.start(5000)

    def go_to_connections(self):
        """Navega para a aba de conexões"""
        self.ui.tabHome.setCurrentIndex(2)


    def populate_acls_table(self):
        """Preenche as tabelas separando ACLs criadas pelo programa (tabela1) 
        e regras existentes do Windows (tabela2)"""

        self.ui.tableWidget.setUpdatesEnabled(False)
        self.ui.tableWidget_2.setUpdatesEnabled(False)

        try:
            self.ui.tableWidget.setRowCount(0)

            nossas_acls = self.carregar_acls()
            for acl in nossas_acls:
                row = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row)
                
                self.ui.table_Conexoes.setSortingEnabled(False)
                self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(acl["nome"]))
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(acl["comeco_ip"]))
                self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(acl["final_ip"]))
                self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(acl["protocolo"].upper()))
                self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(acl["direcao"].upper()))
                self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(acl["acao"]))
                self.ui.tableWidget.setItem(row, 6, QTableWidgetItem(acl["portas"]))
                
                for col, value in enumerate([
                    acl["nome"],
                    acl["comeco_ip"],
                    acl["final_ip"],
                    acl["protocolo"].upper(),
                    acl["direcao"].upper(),
                    acl["acao"],
                    acl["portas"]
                ]):
                    item = QTableWidgetItem(str(value))
                    self.ui.tableWidget.setItem(row, col, item)
                    
                    if acl["acao"] == "PERMITIR":
                        item.setBackground(QColor(0, 128, 0))
                        item.setForeground(QColor(255, 255, 255))
                    else:
                        item.setBackground(QColor(255, 0, 0))
                        item.setForeground(QColor(255, 255, 255))

            headers = ["Nome", "IP Início", "IP Fim", "Protocolo", "Direção", "Ação", "Portas"]
            self.ui.tableWidget.setHorizontalHeaderLabels(headers)
            
            for col in range(7):
                self.ui.tableWidget.setColumnWidth(col, 150)
                
            self.ui.tableWidget.setColumnWidth(0, 200)

        except Exception as e:
            self.logger.error("Não foi possível carregar as ACLs", service="ACL Management", error=str(e))
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar as ACLs:\n{str(e)}")

        self.ui.tableWidget.setUpdatesEnabled(True)
        self.ui.tableWidget_2.setUpdatesEnabled(True)
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.sortItems(0, Qt.AscendingOrder)
        self.ui.tableWidget_2.sortItems(0, Qt.AscendingOrder)
        self.ui.tableWidget.viewport().update()
        self.ui.tableWidget_2.viewport().update()

    def populate_acls_table2(self):
        """Preenche a tabela com todas as regras do Windows Firewall"""
        try:
            fw_policy = win32com.client.Dispatch("HNetCfg.FwPolicy2")
            rules = fw_policy.Rules
            
            self.ui.tableWidget_2.setRowCount(0)
            
            for rule in rules:
                row = self.ui.tableWidget_2.rowCount()
                self.ui.tableWidget_2.insertRow(row)
                
                name = rule.Name
                remote_ips = rule.RemoteAddresses
                protocol = self._get_protocol_name(rule.Protocol)
                direction = "IN" if rule.Direction == 1 else "OUT"
                action = "PERMITIR" if rule.Action == 1 else "BLOQUEAR"
                ports = rule.LocalPorts if rule.LocalPorts else "Todos"
                
                if "-" in remote_ips:
                    start_ip, end_ip = remote_ips.split("-")
                elif "," in remote_ips:
                    start_ip = remote_ips.split(",")[0]
                    end_ip = remote_ips.split(",")[-1]
                else:
                    start_ip = remote_ips
                    end_ip = remote_ips
                
                self.ui.tableWidget_2.setSortingEnabled(False)
                self.ui.tableWidget_2.setItem(row, 0, QTableWidgetItem(name))
                self.ui.tableWidget_2.setItem(row, 1, QTableWidgetItem(start_ip))
                self.ui.tableWidget_2.setItem(row, 2, QTableWidgetItem(end_ip))
                self.ui.tableWidget_2.setItem(row, 3, QTableWidgetItem(protocol))
                self.ui.tableWidget_2.setItem(row, 4, QTableWidgetItem(direction))
                self.ui.tableWidget_2.setItem(row, 5, QTableWidgetItem(action))
                self.ui.tableWidget_2.setItem(row, 6, QTableWidgetItem(ports))
                
                if "ACL criada pelo sistema" in rule.Description:
                    for col in range(7):
                        item = self.ui.tableWidget_2.item(row, col)
                        if item:
                            item.setBackground(QColor(200, 255, 200))
                
                if rule.Action == 0:
                    for col in range(7):
                        item = self.ui.tableWidget_2.item(row, col)
                        if item:
                            item.setForeground(QColor(255, 0, 0))
            
            headers = ["Nome", "IP Início", "IP Fim", "Protocolo", "Direção", "Ação", "Portas"]
            self.ui.tableWidget_2.setHorizontalHeaderLabels(headers)
            self.ui.tableWidget_2.setColumnWidth(0, 150)
            self.ui.tableWidget_2.setColumnWidth(6, 100)
            self.ui.tableWidget_2.setSortingEnabled(True)
            
        except Exception as e:
            self.logger.error("Não foi possível carregar as ACLs", service="ACL Management", error=str(e))
            QMessageBox.critical(self.ui, "Erro", f"Não foi possível carregar as ACLs:\n{str(e)}")

    def _get_protocol_name(self, protocol_code):
        """Converte código de protocolo para nome"""
        protocol_map = {
            1: "ICMP",
            6: "TCP",
            17: "UDP",
            256: "Qualquer",
            -1: "Qualquer"
        }
        return protocol_map.get(protocol_code, str(protocol_code))
    
    def importar_ACL(self):
        try:
            self.logger.info("Iniciando importação de ACLs", service="ACL Management")
            
            root = tk.Tk()
            root.withdraw()

            caminho_arquivo = filedialog.askopenfilename(
                title="Selecione o arquivo de ACLs",
                filetypes=[("Arquivos JSON", "*.json")]
            )

            if not caminho_arquivo:
                self.logger.info("Importação de ACLs cancelada pelo usuário", service="ACL Management")
                return

            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                acls_importadas = json.load(arquivo)

            acls_existentes = self.carregar_acls()
            nomes_existentes = {acl["nome"] for acl in acls_existentes}

            for acl in acls_importadas:
                try:
                    nome_acl = acl.get("nome", "ACL_Sem_Nome")
                    comeco_ip = acl.get("comeco_ip")
                    final_ip = acl.get("final_ip")
                    protocolo = acl.get("protocolo", "qualquer").lower()
                    direcao = acl.get("direcao", "in").lower()
                    acao_texto = acl.get("acao", "PERMITIR").upper()
                    portas = acl.get("portas", "")
                    
                    if nome_acl in nomes_existentes:
                        self.logger.warning(f"ACL '{nome_acl}' já existe e será ignorada", service="ACL Management")
                        continue

                    acao = 1 if acao_texto == "PERMITIR" else 0

                    protocol_map = {"tcp": "TCP", "udp": "UDP", "icmp": "ICMPv4", "qualquer": "ANY"}
                    protocol = protocol_map.get(protocolo, "ANY")

                    action = "allow" if acao == 1 else "block"
                    direction = "in" if direcao == "in" else "out"

                    cmd = [
                        'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                        f'name={nome_acl}',
                        f'dir={direction}',
                        f'action={action}',
                        f'protocol={protocol}',
                        'enable=yes'
                    ]

                    if final_ip and final_ip != comeco_ip:
                        cmd.append(f'remoteip={comeco_ip}-{final_ip}')
                    else:
                        cmd.append(f'remoteip={comeco_ip}')

                    if protocol in ("TCP", "UDP") and portas:
                        cmd.append(f'localport={portas}')

                    result = subprocess.run(cmd, check=True, capture_output=True, text=True, shell=True)

                    if result.returncode == 0:
                        self.logger.info(f"ACL '{nome_acl}' aplicada com sucesso", service="ACL Management")
                        
                        acl_data = {
                            "nome": nome_acl,
                            "comeco_ip": comeco_ip,
                            "final_ip": final_ip,
                            "protocolo": protocolo,
                            "direcao": direcao,
                            "acao": acao_texto,
                            "portas": portas if portas else "Todos",
                            "descricao": f"ACL importada. IPs: {comeco_ip}-{final_ip if final_ip else comeco_ip}"
                        }
                        
                        self.adicionar_acl_arquivo(acl_data)
                        nomes_existentes.add(nome_acl)
                    else:
                        self.logger.error(f"Erro ao aplicar ACL '{nome_acl}'", service="ACL Management", error=result.stderr)

                except subprocess.CalledProcessError as e:
                    self.logger.error(f"Erro de subprocesso ao aplicar '{nome_acl}'", service="ACL Management", error=e.stderr)
                except Exception as e:
                    self.logger.error(f"Erro ao aplicar ACL '{nome_acl}'", service="ACL Management", error=str(e))

            self.populate_acls_table()
            self.logger.info("ACLs importadas com sucesso", service="ACL Management", additional_data={"file_path": caminho_arquivo})
            QMessageBox.information(self, "Sucesso", "ACLs importadas com sucesso!")

        except Exception as e:
            self.logger.error("Falha ao importar ACLs", service="ACL Management", error=str(e))
            QMessageBox.critical(self, "Erro", f"Falha ao importar ACLs:\n{str(e)}")
    
    def criar_acl_netsh(self, nome_acl, comeco_ip, final_ip, protocolo, direcao, acao, portas=None):
        """Cria regra de firewall usando netsh"""
        try:
            action = "allow" if acao == 1 else "block"
            direction = "in" if direcao.lower() == "in" else "out"
            protocol_map = {"tcp": "TCP", "udp": "UDP", "icmp": "ICMPv4", "qualquer": "ANY"}
            protocol = protocol_map.get(protocolo.lower(), "ANY")
            
            cmd = [
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name={nome_acl}',
                f'dir={direction}',
                f'action={action}',
                f'protocol={protocol}',
                'enable=yes'
            ]
            
            if final_ip and final_ip != comeco_ip:
                cmd.append(f'remoteip={comeco_ip}-{final_ip}')
            else:
                cmd.append(f'remoteip={comeco_ip}')
            
            if protocol in ("TCP", "UDP") and portas:
                cmd.append(f'localport={portas}')
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                return True
            else:
                raise Exception(result.stderr)
                
        except subprocess.CalledProcessError as e:
            raise Exception(f"Falha ao executar netsh: {e.stderr}")
        except Exception as e:
            raise Exception(f"Erro ao criar regra: {str(e)}")

    def criar_acl(self):
        """Cria uma nova regra no Windows Firewall usando netsh"""
        if not self.verificar_privilegios():
            self.logger.error("Tentativa de criar ACL sem privilégios", service="ACL Management", suggestion="Executar como administrador")
            QMessageBox.critical(self, "Erro", "Este programa requer privilégios de administrador!")
            return

        nome_acl = self.ui.lineEdit_nomeACL.text().strip()
        comeco_ip = self.ui.lineEdit_comecoIP.text().strip()
        final_ip = self.ui.lineEdit_FinalIP.text().strip()
        protocolo = self.ui.comboBox_protocolo.currentText().lower()
        direcao = self.ui.comboBox_direcao.currentText().lower()
        acao = 1 if self.ui.comboBox_acao.currentIndex() == 0 else 0

        nossas_acls = self.carregar_acls()
        if any(acl["nome"] == nome_acl for acl in nossas_acls):
            self.logger.warning(f"Já existe uma ACL com o nome '{nome_acl}'", service="ACL Management")
            QMessageBox.warning(self, "Aviso", f"Já existe uma ACL com o nome '{nome_acl}' no arquivo!")
            return

        if not nome_acl or not comeco_ip:
            self.logger.warning("Nome da ACL e IP de início são obrigatórios", service="ACL Management")
            QMessageBox.warning(self, "Aviso", "Nome da ACL e IP de início são obrigatórios!")
            return
        
        if not self.validar_ip(comeco_ip):
            self.logger.warning("IP de início inválido", service="ACL Management", additional_data={"ip": comeco_ip})
            QMessageBox.warning(self, "Aviso", "IP de início inválido!")
            return

        if final_ip and not self.validar_ip(final_ip):
            self.logger.warning("IP final inválido", service="ACL Management", additional_data={"ip": final_ip})
            QMessageBox.warning(self, "Aviso", "IP final inválido!")
            return

        portas = []
        if self.ui.checkBox_HTTP.isChecked(): portas.append("80")
        if self.ui.checkBox_FTP.isChecked(): portas.append("21")
        if self.ui.checkBox_SSH.isChecked(): portas.append("22")
        if self.ui.checkBox_Telnet.isChecked(): portas.append("23")
        if self.ui.checkBox_DNS.isChecked(): portas.append("53")
        
        if self.ui.lineEdit_outros.text():
            portas.extend([p.strip() for p in self.ui.lineEdit_outros.text().split(",") if p.strip()])

        portas_str = ",".join(portas) if portas else ""
        
        if portas_str and not self.validar_portas(portas_str):
            self.logger.warning("Portas inválidas", service="ACL Management", additional_data={"portas": portas_str})
            QMessageBox.warning(self, "Aviso", "Portas inválidas! Devem estar entre 1 e 65535.")
            return

        try:
            self.logger.info("Tentativa de criar ACL", service="ACL Management", additional_data={"acl_name": nome_acl})
            
            self.criar_acl_netsh(nome_acl, comeco_ip, final_ip, protocolo, direcao, acao, portas_str)
            
            acl_data = {
                "nome": nome_acl,
                "comeco_ip": comeco_ip,
                "final_ip": final_ip,
                "protocolo": protocolo,
                "direcao": direcao,
                "acao": "PERMITIR" if acao == 1 else "BLOQUEAR",
                "portas": portas_str if portas_str else "Todos",
                "descricao": f"ACL criada pelo sistema. IPs: {comeco_ip}-{final_ip if final_ip else comeco_ip}"
            }
            self.adicionar_acl_arquivo(acl_data)

            self.populate_acls_table()
            self.limpar_campos()
            
            self.logger.info("ACL criada com sucesso", service="ACL Management", additional_data={
                "acl_name": nome_acl,
                "start_ip": comeco_ip,
                "end_ip": final_ip,
                "protocol": protocolo,
                "direction": direcao,
                "action": "PERMITIR" if acao == 1 else "BLOQUEAR",
                "ports": portas_str
            })
            
            QMessageBox.information(self, "Sucesso", f"ACL '{nome_acl}' criada com sucesso!")

        except Exception as e:
            self.logger.error("Falha ao criar ACL", service="ACL Management", error=str(e), additional_data={"acl_name": nome_acl})
            QMessageBox.critical(self, "Erro", f"Falha ao criar regra:\n{str(e)}")

    def validar_portas(self, portas_str):
        """Valida uma string de portas ou intervalos de portas"""
        if not portas_str or portas_str.lower() == "todos":
            return True
            
        for porta in portas_str.split(','):
            porta = porta.strip()
            if '-' in porta:
                try:
                    inicio, fim = map(int, porta.split('-'))
                    if not (1 <= inicio <= 65535) or not (1 <= fim <= 65535) or inicio > fim:
                        return False
                except:
                    return False
            else:
                try:
                    if not (1 <= int(porta) <= 65535):
                        return False
                except:
                    return False
        return True

    def excluir_acl_por_nome(self):
        """Exclui uma ACL pelo nome, removendo do firewall, tabela e arquivo"""
        nome_acl, ok = QInputDialog.getText(
            self,
            "Excluir ACL",
            "Digite o nome exato da ACL que deseja excluir:",
            QLineEdit.Normal,
            ""
        )
        
        if not ok or not nome_acl:
            return
        
        self.logger.info("Tentativa de excluir ACL", service="ACL Management", additional_data={"acl_name": nome_acl})

        try:
            self.remover_acl_firewall(nome_acl)
            self.remover_acl_arquivo(nome_acl)
            self.remover_acl_tabela(nome_acl)
            
            self.logger.info("ACL removida com sucesso", service="ACL Management", additional_data={"acl_name": nome_acl})
            
            QMessageBox.information(
                self,
                "Sucesso",
                f"ACL '{nome_acl}' foi removida do firewall, arquivo e tabela!"
            )
            
        except Exception as e:
            self.logger.error("Falha ao excluir ACL", service="ACL Management", error=str(e), additional_data={"acl_name": nome_acl})
            QMessageBox.critical(
                self,
                "Erro",
                f"Falha ao excluir ACL:\n{str(e)}"
            )

    def remover_acl_firewall(self, nome_acl):
        """Remove a regra do firewall usando netsh"""
        try:
            result = subprocess.run(
                ['netsh', 'advfirewall', 'firewall', 'delete', 'rule', f'name={nome_acl}'],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode != 0:
                if "No rules match" in result.stderr:
                    raise Exception(f"Regra '{nome_acl}' não encontrada no firewall")
                else:
                    raise Exception(f"Erro netsh: {result.stderr}")
        
        except subprocess.CalledProcessError as e:
            raise Exception(f"Falha ao executar netsh: {e.stderr}")

    def remover_acl_arquivo(self, nome_acl):
        """Remove a ACL do arquivo JSON"""
        acls = self.carregar_acls()
        novas_acls = [acl for acl in acls if acl["nome"] != nome_acl]
        
        if len(acls) == len(novas_acls):
            raise Exception(f"ACL '{nome_acl}' não encontrada no arquivo")
        
        self.salvar_acls(novas_acls)

    def remover_acl_tabela(self, nome_acl):
        """Remove a ACL da tabela visual"""
        for row in range(self.ui.tableWidget.rowCount()):
            if self.ui.tableWidget.item(row, 0).text() == nome_acl:
                self.ui.tableWidget.removeRow(row)
                return
        
        raise Exception(f"ACL '{nome_acl}' não encontrada na tabela")

    def preparar_edicao(self, row, column):
        """Prepara a interface para editar uma ACL existente"""
        self.linha_editando = row
    
        reply = QMessageBox.question(
            self,
            "Editar ACL",
            "Deseja editar esta ACL?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
    
        if reply == QMessageBox.StandardButton.Yes:
            self.carregar_dados_para_edicao(row)

    def carregar_dados_para_edicao(self, row):
        """Carrega os dados da ACL selecionada nos campos de edição"""
        try:
            nome_item = self.ui.tableWidget.item(row, 0)
            inicio_ip_item = self.ui.tableWidget.item(row, 1)
            final_ip_item = self.ui.tableWidget.item(row, 2)
            protocolo_item = self.ui.tableWidget.item(row, 3)
            direcao_item = self.ui.tableWidget.item(row, 4)
            acao_item = self.ui.tableWidget.item(row, 5)
            servicos_item = self.ui.tableWidget.item(row, 6)
            
            if None in (nome_item, inicio_ip_item, protocolo_item, direcao_item, acao_item, servicos_item):
                raise ValueError("Dados incompletos na tabela")
                
            nome = nome_item.text()
            inicio_ip = inicio_ip_item.text()
            final_ip = final_ip_item.text() if final_ip_item else ""
            protocolo = protocolo_item.text()
            direcao = direcao_item.text()
            acao = acao_item.text()
            servicos = servicos_item.text()

            self.ui.lineEdit_nomeACL.setText(nome)
            self.ui.lineEdit_comecoIP.setText(inicio_ip)
            self.ui.lineEdit_FinalIP.setText(final_ip if final_ip and final_ip != inicio_ip else "")

            index_protocolo = self.ui.comboBox_protocolo.findText(protocolo, Qt.MatchFixedString)
            if index_protocolo >= 0:
                self.ui.comboBox_protocolo.setCurrentIndex(index_protocolo)
            else:
                self.ui.comboBox_protocolo.setCurrentIndex(0)

            index_direcao = self.ui.comboBox_direcao.findText(direcao, Qt.MatchFixedString)
            if index_direcao >= 0:
                self.ui.comboBox_direcao.setCurrentIndex(index_direcao)
            else:
                self.ui.comboBox_direcao.setCurrentIndex(0)

            if hasattr(self.ui, 'radioButton_permitir') and hasattr(self.ui, 'radioButton_bloquear'):
                if acao == "BLOQUEAR":
                    self.ui.radioButton_bloquear.setChecked(True)
                else:
                    self.ui.radioButton_permitir.setChecked(True)
            elif hasattr(self.ui, 'comboBox_acao'):
                index = 1 if acao == "BLOQUEAR" else 0
                self.ui.comboBox_acao.setCurrentIndex(index)

            servicos_lista = [s.strip() for s in servicos.split(",") if s.strip()]
            
            for checkbox in [self.ui.checkBox_HTTP, self.ui.checkBox_FTP, 
                            self.ui.checkBox_SSH, self.ui.checkBox_Telnet, 
                            self.ui.checkBox_DNS]:
                checkbox.setChecked(False)
            
            self.ui.lineEdit_outros.clear()
            outras_portas = []
            
            porta_servico = {
                "80": self.ui.checkBox_HTTP,
                "21": self.ui.checkBox_FTP,
                "22": self.ui.checkBox_SSH,
                "23": self.ui.checkBox_Telnet,
                "53": self.ui.checkBox_DNS,
            }
            
            for porta in servicos_lista:
                if porta in porta_servico:
                    porta_servico[porta].setChecked(True)
                elif porta != "Todos" and porta:
                    outras_portas.append(porta)
            
            if outras_portas:
                self.ui.lineEdit_outros.setText(",".join(outras_portas))

            self.ui.button_CriarACL.setText("Salvar Edição")
            if self.ui.button_CriarACL.clicked:
                try:
                    self.ui.button_CriarACL.clicked.disconnect()
                except:
                    pass
            self.ui.button_CriarACL.clicked.connect(self.salvar_edicao)

        except Exception as e:
            self.logger.error("Falha ao carregar dados para edição", service="ACL Management", error=str(e))
            QMessageBox.critical(self, "Erro", f"Falha ao carregar dados para edição:\n{str(e)}")

    def salvar_edicao(self):
        """Salva as alterações de uma ACL editada"""
        if not hasattr(self, 'linha_editando'):
            self.logger.warning("Nenhuma ACL selecionada para edição", service="ACL Management")
            QMessageBox.warning(self, "Erro", "Nenhuma ACL selecionada para edição")
            return

        try:
            nome_antigo = self.ui.tableWidget.item(self.linha_editando, 0).text()
            
            try:
                subprocess.run(
                    ['netsh', 'advfirewall', 'firewall', 'delete', 'rule', f'name={nome_antigo}'],
                    check=True,
                    shell=True
                )
                
                acls = self.carregar_acls()
                acls = [acl for acl in acls if acl["nome"] != nome_antigo]
                self.salvar_acls(acls)
                
            except Exception as e:
                self.logger.error("Falha ao remover regra antiga", service="ACL Management", error=str(e))
                QMessageBox.critical(self, "Erro", f"Falha ao remover regra antiga:\n{str(e)}")
                return

            self.criar_acl()
            
            self.ui.button_CriarACL.setText("Criar ACL")
            if self.ui.button_CriarACL.clicked:
                try:
                    self.ui.button_CriarACL.clicked.disconnect()
                except:
                    pass
            self.ui.button_CriarACL.clicked.connect(self.criar_acl)

            if hasattr(self, 'linha_editando'):
                del self.linha_editando
                
            self.logger.info("ACL editada com sucesso", service="ACL Management", additional_data={"old_name": nome_antigo})
            QMessageBox.information(self, "Sucesso", "ACL editada com sucesso!")

        except Exception as e:
            self.logger.error("Falha ao salvar edição", service="ACL Management", error=str(e))
            QMessageBox.critical(self, "Erro", f"Falha ao salvar edição:\n{str(e)}")

    def limpar_campos(self):
        """Limpa todos os campos de entrada"""
        self.ui.lineEdit_nomeACL.clear()
        self.ui.lineEdit_comecoIP.clear()
        self.ui.lineEdit_FinalIP.clear()
        self.ui.comboBox_protocolo.setCurrentIndex(0)
        self.ui.comboBox_direcao.setCurrentIndex(0)
    
        self.ui.checkBox_HTTP.setChecked(False)
        self.ui.checkBox_FTP.setChecked(False)
        self.ui.checkBox_SSH.setChecked(False)
        self.ui.checkBox_Telnet.setChecked(False)
        self.ui.checkBox_DNS.setChecked(False)
        self.ui.lineEdit_outros.clear()

    def validar_ip(self, ip):
        """Valida um endereço IP"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                if not part.isdigit() or not 0 <= int(part) <= 255:
                    return False
            return True
        except:
            return False
        
    def carregar_acls(self):
        """Carrega as ACLs do arquivo, criando-o se não existir"""
        acls_file = "acls_salvas.json"
        
        try:
            if not os.path.exists(acls_file):
                with open(acls_file, 'w') as f:
                    json.dump([], f)
                return []
            
            with open(acls_file, 'r') as f:
                return json.load(f)
                
        except json.JSONDecodeError:
            with open(acls_file, 'w') as f:
                json.dump([], f)
            return []
        except Exception as e:
            self.logger.error("Erro ao carregar ACLs", service="ACL Management", error=str(e))
            return []

    def salvar_acls(self, acls):
        """Salva as ACLs no arquivo, garantindo que ele exista"""
        acls_file = "acls_salvas.json"
        
        try:
            os.makedirs(os.path.dirname(acls_file), exist_ok=True)
            
            with open(acls_file, 'w') as f:
                json.dump(acls, f, indent=4)
        except Exception as e:
            self.logger.error("Erro ao salvar ACLs", service="ACL Management", error=str(e))
            try:
                backup_file = os.path.join(os.path.expanduser(""), "acls_salvas.json")
                with open(backup_file, 'w') as f:
                    json.dump(acls, f, indent=4)
                self.logger.info("Backup de ACLs salvo", service="ACL Management", additional_data={"backup_path": backup_file})
            except:
                self.logger.error("Falha ao criar backup de ACLs", service="ACL Management")

    def adicionar_acl_arquivo(self, acl_data):
        """Adiciona uma nova ACL ao arquivo de persistência"""
        acls = self.carregar_acls()
        acls.append(acl_data)
        self.salvar_acls(acls)
    
    def verificar_privilegios(self):
        """Verifica se o programa está sendo executado como administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def update_table(self):
        try:
            result = subprocess.run(
                ['netstat', '-ano'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            lines = result.stdout.splitlines()
            self.ui.table_Conexoes.setRowCount(0)
            current_time = time.time()
            
            active_pids = set()
            for line in lines[4:]:
                parts = list(filter(None, line.split()))
                if len(parts) >= 5 and parts[4].isdigit():
                    active_pids.add(int(parts[4]))
            
            for proc in psutil.process_iter(['pid', 'name', 'io_counters']):
                try:
                    if proc.info['io_counters'].read_bytes > 0 or proc.info['io_counters'].write_bytes > 0:
                        active_pids.add(proc.info['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
                    continue
            
            for pid in active_pids:
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                    
                    io_counters = process.io_counters()
                    current_upload = io_counters.write_bytes
                    current_download = io_counters.read_bytes
                    
                    if pid not in self.network_stats:
                        self.network_stats[pid] = {
                            'last_upload': current_upload,
                            'last_download': current_download,
                            'timestamp': current_time
                        }
                        upload_speed = "0.00 B/s"
                        download_speed = "0.00 B/s"
                    else:
                        last_stats = self.network_stats[pid]
                        time_diff = current_time - last_stats['timestamp']
                        
                        if time_diff > 0:
                            upload_diff = current_upload - last_stats['last_upload']
                            download_diff = current_download - last_stats['last_download']
                            
                            upload_speed_bps = upload_diff / time_diff
                            download_speed_bps = download_diff / time_diff
                            
                            upload_speed = self.format_speed(upload_speed_bps)
                            download_speed = self.format_speed(download_speed_bps)
                       
                    
                    self.network_stats[pid] = {
                        'last_upload': current_upload,
                        'last_download': current_download,
                        'timestamp': current_time
                    }
                    
                    connections = []
                    try:
                        connections = process.net_connections()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                    
                    if not connections:
                        row = self.ui.table_Conexoes.rowCount()
                        self.ui.table_Conexoes.insertRow(row)
                        
                        self.ui.table_Conexoes.setItem(row, 0, QTableWidgetItem(process_name))
                        self.ui.table_Conexoes.setItem(row, 1, QTableWidgetItem("N/A"))
                        self.ui.table_Conexoes.setItem(row, 2, QTableWidgetItem("N/A"))
                        self.ui.table_Conexoes.setItem(row, 3, QTableWidgetItem("N/A"))
                        self.ui.table_Conexoes.setItem(row, 4, QTableWidgetItem(str(pid)))
                        self.ui.table_Conexoes.setItem(row, 5, QTableWidgetItem(upload_speed))
                        self.ui.table_Conexoes.setItem(row, 6, QTableWidgetItem(download_speed))
                    
                    for conn in connections:
                        row = self.ui.table_Conexoes.rowCount()
                        self.ui.table_Conexoes.insertRow(row)
                        
                        conn_type = "UDP"
                        if conn.type == 1:  # SOCK_STREAM (TCP)
                            conn_type = "TCP"
                        elif conn.type == 2:  # SOCK_DGRAM (UDP)
                            conn_type = "UDP"
                        
                        self.ui.table_Conexoes.setItem(row, 0, QTableWidgetItem(process_name))
                        self.ui.table_Conexoes.setItem(row, 1, QTableWidgetItem(conn_type))
                        
                        remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                        self.ui.table_Conexoes.setItem(row, 2, QTableWidgetItem(
                            f"{conn.laddr.ip}:{conn.laddr.port} → {remote_addr}"))
                        
                        conn_status = getattr(conn, 'status', "N/A")
                        self.ui.table_Conexoes.setItem(row, 3, QTableWidgetItem(conn_status))
                        self.ui.table_Conexoes.setItem(row, 4, QTableWidgetItem(str(pid)))
                        self.ui.table_Conexoes.setItem(row, 5, QTableWidgetItem(download_speed))
                        self.ui.table_Conexoes.setItem(row, 6, QTableWidgetItem(upload_speed))
                        
                        if conn_status == "ESTABLISHED":
                            for col in range(7):
                                item = self.ui.table_Conexoes.item(row, col)
                                if item:
                                    item.setBackground(QColor(255, 215, 0, 50))
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError) as e:
                    self.logger.error(f"Processo {pid}: {e}", service="Process Management")
                    continue
        
        except Exception as e:
            self.logger.error("Error updating table", service="Process Management", error=str(e))

    def format_speed(self, speed_bps):
        """Formata a velocidade em unidades legíveis"""
        if speed_bps >= 1024*1024:
            return f"{speed_bps/(1024*1024):.2f} MB/s"
        elif speed_bps >= 1024:
            return f"{speed_bps/1024:.2f} KB/s"
        return f"{speed_bps:.2f} B/s"

    def setup_table(self):
        """Configura a tabela e conexões de sinais"""
        self.ui.table_Conexoes.cellClicked.connect(self._on_cell_clicked)
    
    def _on_cell_clicked(self, row, col):
        pid_item = None
        if col == 0 or col == 1 or col == 2 or col == 3 or col == 4 or col == 5:
            pid_item = self.ui.table_Conexoes.item(row, 4)

        if pid_item is not None:
            pid = pid_item.text()
            confirm_box = QMessageBox()
            confirm_box.setWindowTitle("Confirmar")
            confirm_box.setText(f"Encerrar processo PID {pid}?")
            confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm_box.setDefaultButton(QMessageBox.No)
        
        if confirm_box.exec() == QMessageBox.Yes:
            self._fechar_conexao(pid)
            QMessageBox.information(None, "Sucesso", "Conexão encerrada!")
        else:
            confirm_box.close()

    def _fechar_conexao(self, pid):
        """Lógica para encerrar o processo (Windows)"""
        try:
            self.logger.info("Tentativa de encerrar processo", service="Process Management", additional_data={"pid": pid})
            
            confirm = QMessageBox.question(
                None, 
                "Confirmar", 
                f"Encerrar processo PID {pid}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                subprocess.run(f"taskkill /PID {pid} /F", shell=True, check=True)
                self.logger.info("Processo encerrado com sucesso", service="Process Management", additional_data={"pid": pid})
                QMessageBox.information(None, "Sucesso", "Conexão encerrada!")
                self.update_table()
        except subprocess.CalledProcessError as e:
            self.logger.error("Falha ao encerrar processo", service="Process Management", error=str(e), additional_data={"pid": pid})
            QMessageBox.critical(None, "Erro", f"Falha ao encerrar: {e}")
    
    def on_tab_changed(self, index):
        if index == 3:
            self.populate_reports_table()
    
    def generate_report(self):
        """Gera um relatório PDF detalhado com estatísticas e eventos importantes"""
        try:
            self.logger.info("Iniciando geração de relatório", service="Reporting")
            
            # Solicitar local para salvar o arquivo
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Relatório como PDF",
                f"relatorio_seguranca_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                "Arquivos PDF (*.pdf)"
            )
            
            if not filename:
                return
            
            if not filename.lower().endswith('.pdf'):
                filename += '.pdf'
            
            # Verificar se o arquivo de logs existe
            log_file = "firewall_logs.json"
            if not os.path.exists(log_file):
                self.logger.error("Arquivo de logs não encontrado", service="Reporting")
                QMessageBox.critical(self, "Erro", "Arquivo de logs não encontrado!")
                return
            
            # Carregar os logs
            with open(log_file, 'r') as f:
                logs = [json.loads(line) for line in f if line.strip()]
            
            if not logs:
                QMessageBox.information(self, "Aviso", "Nenhum dado de log disponível para gerar relatório!")
                return
            
            # Processar os logs para estatísticas
            report_data = self._analyze_logs_for_report(logs)
            
            # Criar o documento PDF
            doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)
            
            styles = getSampleStyleSheet()
            elements = []
            
            # Adicionar cabeçalho
            header_style = ParagraphStyle(
                'Header',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor("#1E3F66"),
                spaceAfter=20,
                alignment=TA_CENTER
            )
            
            header = Paragraph("Relatório de Segurança - TecSec Tecguard", header_style)
            elements.append(header)
            
            # Adicionar informações básicas
            date_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            basic_info = [
                Paragraph(f"<b>Data de geração:</b> {date_str}", styles['Normal']),
                Paragraph(f"<b>Período coberto:</b> {report_data['period']}", styles['Normal']),
                Paragraph(f"<b>Total de eventos:</b> {len(logs)}", styles['Normal']),
                Spacer(1, 20)
            ]
            elements.extend(basic_info)
            
            # Adicionar estatísticas
            stats_style = ParagraphStyle(
                'StatsHeader',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor("#2E5894"),
                spaceAfter=10
            )
            
            elements.append(Paragraph("Estatísticas Principais", stats_style))
            
            # Tabela de estatísticas
            stats_data = [
                ["Eventos Críticos", str(report_data['critical_count'])],
                ["Alertas", str(report_data['warning_count'])],
                ["Eventos Suspeitos", str(report_data['suspicious_count'])],
                ["Eventos Informativos", str(report_data['info_count'])],
                ["Erros", str(report_data['error_count'])]
            ]
            
            stats_table = Table(stats_data, colWidths=[200, 100])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B9CD3")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#E6F2FA")),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#C9E0F5")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 20))
            
            # Adicionar seção de eventos mais comuns
            elements.append(Paragraph("Eventos Mais Frequentes", stats_style))
            
            freq_table_data = [["Evento", "Ocorrências"]] + report_data['top_events']
            freq_table = Table(freq_table_data, colWidths=[300, 100])
            freq_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B9CD3")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F5F9FD")),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#D9E6F2")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(freq_table)
            elements.append(Spacer(1, 20))
            
            # Adicionar seção de eventos mais perigosos
            elements.append(Paragraph("Eventos Mais Críticos", stats_style))
            
            danger_table_data = [["Data/Hora", "Evento", "Classificação", "IP", "Porta"]]
            for event in report_data['critical_events']:
                danger_table_data.append([
                    event.get('timestamp', 'N/A'),
                    event.get('event', 'N/A'),
                    event.get('classification', 'N/A'),
                    event.get('ip', 'N/A'),
                    event.get('port', 'N/A')
                ])
            
            danger_table = Table(danger_table_data, colWidths=[100, 150, 80, 100, 60])
            danger_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#D9534F")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (4, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#FDF5F5")),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#F5D9D9")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor("#D9534F")),
            ]))
            elements.append(danger_table)
            elements.append(Spacer(1, 20))
            
            # Adicionar seção de IPs suspeitos
            elements.append(Paragraph("IPs Mais Ativos", stats_style))
            
            ip_table_data = [["IP", "Eventos", "Último Evento"]] + report_data['top_ips']
            ip_table = Table(ip_table_data, colWidths=[120, 80, 200])
            ip_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5BC0DE")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F0F8FB")),
                
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#D0E9F3")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(ip_table)
            elements.append(Spacer(1, 20))
            
            # Adicionar rodapé
            footer = Paragraph("<i>Relatório gerado automaticamente pelo TecSec Tecguard - Sistema de Monitoramento de Segurança</i>", 
                            styles['Italic'])
            elements.append(footer)
            
            # Gerar o PDF
            doc.build(elements)
            
            self.logger.info("Relatório gerado com sucesso", 
                            service="Reporting", 
                            additional_data={
                                "file_path": os.path.abspath(filename),
                                "stats": {
                                    "total_events": len(logs),
                                    "critical_events": report_data['critical_count'],
                                    "top_events": report_data['top_events']
                                }
                            })
            
            QMessageBox.information(
                self, 
                "Relatório Gerado", 
                f"Relatório gerado com sucesso!\n\nArquivo salvo em:\n{os.path.abspath(filename)}"
            )
            
        except Exception as e:
            self.logger.error("Erro ao gerar relatório", service="Reporting", error=str(e))
            QMessageBox.critical(
                self,
                "Erro ao Gerar Relatório",
                f"Ocorreu um erro ao gerar o relatório:\n{str(e)}"
            )

    def _analyze_logs_for_report(self, logs):
        """Analisa os logs e extrai dados para o relatório"""
        # Determinar período coberto
        if logs:
            first_date = datetime.fromisoformat(logs[-1]['timestamp'])
            last_date = datetime.fromisoformat(logs[0]['timestamp'])
            period = f"{first_date.strftime('%d/%m/%Y')} a {last_date.strftime('%d/%m/%Y')}"
        else:
            period = "N/A"
        
        # Contar eventos por classificação
        classifications = {
            'Ataque': 0,
            'Alerta': 0,
            'Suspeito': 0,
            'Informativo': 0,
            'Erro': 0
        }
        
        for log in logs:
            classification = log.get('classification', '').lower()
            if 'ataque' in classification:
                classifications['Ataque'] += 1
            elif 'alerta' in classification:
                classifications['Alerta'] += 1
            elif 'suspeito' in classification:
                classifications['Suspeito'] += 1
            elif 'informativo' in classification:
                classifications['Informativo'] += 1
            elif 'erro' in classification:
                classifications['Erro'] += 1
        
        # Contar eventos mais comuns
        event_counts = {}
        for log in logs:
            event = log.get('event', 'Desconhecido')
            event_counts[event] = event_counts.get(event, 0) + 1
        
        top_events = sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Identificar eventos críticos
        critical_events = []
        for log in logs:
            classification = log.get('classification', '').lower()
            if 'ataque' in classification or 'alerta' in classification:
                critical_events.append(log)
        
        # Ordenar por data (mais recente primeiro) e pegar os 5 mais recentes
        critical_events = sorted(critical_events, 
                            key=lambda x: x.get('timestamp', ''),
                            reverse=True)[:5]
        
        # Contar IPs mais ativos
        ip_counts = {}
        ip_last_event = {}
        for log in logs:
            ip = log.get('ip', None)
            if ip:
                ip_counts[ip] = ip_counts.get(ip, 0) + 1
                ip_last_event[ip] = log.get('timestamp', 'N/A')
        
        top_ips = []
        for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            top_ips.append([
                ip, 
                str(count), 
                ip_last_event.get(ip, 'N/A')
            ])
        
        return {
            'period': period,
            'critical_count': classifications['Ataque'],
            'warning_count': classifications['Alerta'],
            'suspicious_count': classifications['Suspeito'],
            'info_count': classifications['Informativo'],
            'error_count': classifications['Erro'],
            'top_events': top_events,
            'critical_events': critical_events,
            'top_ips': top_ips
        }
            

    def populate_reports_table(self):
        """Preenche a tabela de relatórios com dados do arquivo JSON de logs"""
        try:
            # Limpa a tabela antes de preencher
            self.ui.tableWidget_relatorio.setRowCount(0)
            
            # Verifica se o arquivo de logs existe
            if not os.path.exists("firewall_logs.json"):
                self.logger.warning("Arquivo de logs não encontrado", service="Reporting")
                return
                
            # Lê o arquivo de logs linha por linha (cada linha é um JSON)
            with open("firewall_logs.json", "r") as f:
                logs = [json.loads(line) for line in f if line.strip()]
                
            # Ordena os logs por timestamp (do mais recente para o mais antigo)
            logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            # Preenche a tabela com os dados dos logs
            for log in logs:
                row = self.ui.tableWidget_relatorio.rowCount()
                self.ui.tableWidget_relatorio.insertRow(row)
                
                # Função auxiliar para tratar valores vazios
                def get_value(key, default="N/A"):
                    value = log.get(key)
                    return default if value is None or value == "" else str(value)
                
                # Formata a data para exibição
                timestamp = get_value("timestamp")
                try:
                    dt = datetime.fromisoformat(timestamp)
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = timestamp if timestamp != "N/A" else "N/A"
                
                # Preenche as células (agora usando get_value)
                self.ui.tableWidget_relatorio.setItem(row, 0, QTableWidgetItem(formatted_time))
                self.ui.tableWidget_relatorio.setItem(row, 1, QTableWidgetItem(get_value("classification")))
                self.ui.tableWidget_relatorio.setItem(row, 2, QTableWidgetItem(get_value("event")))
                self.ui.tableWidget_relatorio.setItem(row, 3, QTableWidgetItem(get_value("ip")))
                self.ui.tableWidget_relatorio.setItem(row, 4, QTableWidgetItem(get_value("port")))
                self.ui.tableWidget_relatorio.setItem(row, 5, QTableWidgetItem(get_value("service")))
                
                # Aplica cor apenas ao texto da classificação
                classification = get_value("classification").lower()
                if classification != "n/a":
                    classification_item = self.ui.tableWidget_relatorio.item(row, 1)
                    bg_color = QColor(0, 128, 0)  # Verde padrão

                    if "ataque" in classification:
                        bg_color = QColor(255, 0, 0)      # Vermelho
                    elif "suspeito" in classification:
                        bg_color = QColor(255, 165, 0)    # Laranja
                    elif "alerta" in classification:
                        bg_color = QColor(218, 165, 32)   # Dourado
                    elif "erro" in classification:
                        bg_color = QColor(139, 0, 139)    # Roxo

                    classification_item.setBackground(bg_color)
                    classification_item.setForeground(QColor(255, 255, 255))
            
            # Ajusta o tamanho das colunas para o conteúdo
            self.ui.tableWidget_relatorio.resizeColumnsToContents()
            self.ui.tableWidget_relatorio.verticalHeader().setVisible(False)
            
        except Exception as e:
            self.logger.error("Erro ao carregar logs na tabela", service="Reporting", error=str(e))
            QMessageBox.critical(self, "Erro", f"Falha ao carregar logs:\n{str(e)}")

    def show_table_context_menu(self, position):
        menu = QMenu(self)
    
        export_action = QAction("Exportar linha para PDF", self)
        copy_action = QAction("Copiar dados da linha", self)
        export_all_action = QAction("Exportar toda a tabela para PDF", self)
    
        menu.addAction(export_action)
        menu.addAction(copy_action)
        menu.addSeparator()
        menu.addAction(export_all_action)
    
        action = menu.exec_(self.tableWidget_relatorio.viewport().mapToGlobal(position))
    
        if action == export_action:
            self.export_row_to_pdf(position)
        elif action == copy_action:
            self.copy_row_data(position)
        elif action == export_all_action:
            self.generate_report()

    def setup_connections(self):
        """Conecta os sinais dos botões e comboboxes"""
        self.ui.button_Conexoes.clicked.connect(self.go_to_connections)
        self.ui.pushButton_relatorio.clicked.connect(self.generate_report)
        self.ui.comboBox_Tema.currentIndexChanged.connect(self.change_theme)
        self.ui.comboBox_operacao.currentIndexChanged.connect(self.change_operation_mode)
        self.ui.comboBox_PerfisRede.currentIndexChanged.connect(self.change_network_profile)
        self.ui.comboBox_Resolucao.currentIndexChanged.connect(self.change_resolution)
        self.ui.comboBox_ModoGamer.currentIndexChanged.connect(self.on_gamer_mode_changed)
    
    def change_resolution(self, index):
        """Altera a resolução da interface"""
        resolution_map = {
            0: ("1360x768", "hd"),
            1: ("1920x1080", "fhd")
        }
        
        selected_resolution, resolution_key = resolution_map.get(index, ("1360x768", "hd"))
        
        if resolution_key != self.config.get("resolution", "hd"):
            self.logger.info("Resolução alterada", service="UI Configuration", additional_data={
                "old_resolution": self.config.get("resolution", "hd"),
                "new_resolution": selected_resolution
            })
            
            self.config["resolution"] = resolution_key
            self.save_config()
            
            msg = QMessageBox()
            msg.setWindowTitle("Reiniciar aplicativo")
            msg.setText("A resolução será aplicada após reiniciar o aplicativo.")
            msg.setInformativeText(f"Resolução selecionada: {selected_resolution}")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            
            resposta = msg.exec()
            
            if resposta == QMessageBox.Yes:
                self.restart_application()
            else:
                current_resolution = self.config.get("resolution", "hd")
                reverse_map = {"hd": 0, "fhd": 1}
                self.ui.comboBox_Resolucao.setCurrentIndex(reverse_map.get(current_resolution, 0))

    def setup_log_management(self):
        """Configura o gerenciamento de logs"""
        # Conecta sinais da interface para configurações de log
        self.ui.comboBox_RetencaoLog.currentIndexChanged.connect(self.change_log_retention)
        self.ui.radioButton_EnvioLogsSim.toggled.connect(self.toggle_log_sending)
        self.ui.lineEdit_IP.textChanged.connect(self.update_log_server)
        self.ui.lineEdit_Porta.textChanged.connect(self.update_log_server)
        self.ui.lineEdit_RetencaoOutros.textChanged.connect(self.update_custom_retention)
        
        # Configura estado inicial dos campos
        settings = self.log_manager.load_config()
        self.ui.radioButton_EnvioLogsSim.setChecked(settings.get("send_logs", False))
        self.ui.radioButton_EnvioLogsNo.setChecked(not settings.get("send_logs", False))
        self.ui.lineEdit_IP.setText(settings.get("log_server_ip", ""))
        self.ui.lineEdit_Porta.setText(settings.get("log_server_port", "514"))
        
        # Mostra/esconde campos conforme configuração
        visible = settings.get("send_logs", False)
        self.ui.lineEdit_IP.setVisible(visible)
        self.ui.lineEdit_Porta.setVisible(visible)
        self.ui.label_IP.setVisible(visible)
        self.ui.label_Porta.setVisible(visible)
    
    def auto_cleanup_logs(self):
        """Limpeza automática de logs antigos"""
        try:
            deleted_count = self.log_manager.cleanup_old_logs()
            if deleted_count > 0:
                self.logger.info(f"Limpeza automática de logs: {deleted_count} logs antigos removidos", 
                               service="Log Management")
        except Exception as e:
            self.logger.error("Erro na limpeza automática de logs", service="Log Management", error=str(e))
    
    def change_log_retention(self, index):
        """Altera o período de retenção de logs"""
        retention_map = {
            0: 3,  # 3 dias
            1: 5,  # 5 dias
            2: 7,  # 7 dias
            3: 15, # 15 dias
            4: 30  # 30 dias
        }
        
        retention_days = retention_map.get(index, 7)
        
        settings = self.log_manager.load_config()
        settings["retention_days"] = retention_days
        self.log_manager.save_config(settings)
        
        self.logger.info("Período de retenção de logs alterado", service="Log Management", 
                       additional_data={"retention_days": retention_days})
        
        # Executa limpeza imediata
        deleted_count = self.log_manager.cleanup_old_logs()
        if deleted_count > 0:
            QMessageBox.information(self, "Limpeza de Logs", 
                                  f"{deleted_count} logs antigos foram removidos.")
    
    def update_custom_retention(self, text):
        """Atualiza retenção personalizada"""
        if text.strip() and text.strip().isdigit():
            retention_days = int(text.strip())
            if 1 <= retention_days <= 365:  # Limite razoável
                settings = self.log_manager.load_config()
                settings["retention_days"] = retention_days
                self.log_manager.save_config(settings)
                
                self.logger.info("Retenção personalizada de logs configurada", service="Log Management",
                               additional_data={"retention_days": retention_days})
    
    def toggle_log_sending(self, checked):
        """Ativa/desativa envio de logs - agora esconde os campos quando desativado"""
        if self.ui.radioButton_EnvioLogsSim.isChecked():
            settings = self.log_manager.load_config()
            settings["send_logs"] = True
            self.log_manager.save_config(settings)
            
            # Mostra campos de configuração do servidor
            self.ui.lineEdit_IP.setVisible(True)
            self.ui.lineEdit_Porta.setVisible(True)
            self.ui.label_IP.setVisible(True)
            self.ui.label_Porta.setVisible(True)
            
            self.logger.info("Envio de logs ativado", service="Log Management")
        else:
            settings = self.log_manager.load_config()
            settings["send_logs"] = False
            self.log_manager.save_config(settings)
            
            # Esconde completamente os campos
            self.ui.lineEdit_IP.setVisible(False)
            self.ui.lineEdit_Porta.setVisible(False)
            self.ui.label_IP.setVisible(False)
            self.ui.label_Porta.setVisible(False)
            
            self.logger.info("Envio de logs desativado", service="Log Management")
    
    def update_log_server(self):
        """Atualiza configurações do servidor de logs"""
        ip = self.ui.lineEdit_IP.text().strip()
        port = self.ui.lineEdit_Porta.text().strip()
        
        if ip and port:
            settings = self.log_manager.load_config()
            settings["log_server_ip"] = ip
            settings["log_server_port"] = port
            self.log_manager.save_config(settings)
            
            self.logger.info("Configurações do servidor de logs atualizadas", service="Log Management",
                           additional_data={"server_ip": ip, "server_port": port})
    
    def show_log_statistics(self):
        """Exibe estatísticas dos logs em uma caixa de diálogo"""
        try:
            stats = self.log_manager.get_log_stats()
            
            msg = QMessageBox()
            msg.setWindowTitle("Estatísticas de Logs")
            msg.setIcon(QMessageBox.Information)
            
            message = f"Total de logs: {stats['total_logs']}\n"
            message += f"Log mais antigo: {stats['oldest_log'] or 'N/A'}\n"
            message += f"Log mais recente: {stats['newest_log'] or 'N/A'}\n\n"
            message += "Logs por classificação:\n"
            
            for classification, count in stats['by_classification'].items():
                message += f"  {classification}: {count}\n"
            
            msg.setText(message)
            msg.exec()
            
        except Exception as e:
            self.logger.error("Erro ao exibir estatísticas de logs", service="Log Management", error=str(e))
            QMessageBox.critical(self, "Erro", f"Falha ao obter estatísticas:\n{str(e)}")
    
    def export_logs(self):
        """Exporta logs para arquivo externo"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Logs",
                f"tecguard_logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "Arquivos JSON (*.json)"
            )
            
            if not filename:
                return
                
            if not filename.lower().endswith('.json'):
                filename += '.json'
            
            # Copia o arquivo de logs
            if os.path.exists(self.log_manager.log_file):
                shutil.copy2(self.log_manager.log_file, filename)
                self.logger.info("Logs exportados com sucesso", service="Log Management",
                               additional_data={"export_file": filename})
                QMessageBox.information(self, "Sucesso", f"Logs exportados para:\n{filename}")
            else:
                QMessageBox.warning(self, "Aviso", "Nenhum log disponível para exportar.")
                
        except Exception as e:
            self.logger.error("Erro ao exportar logs", service="Log Management", error=str(e))
            QMessageBox.critical(self, "Erro", f"Falha ao exportar logs:\n{str(e)}")

    def on_gamer_mode_changed(self, index):
        """Lida com a mudança no modo gamer"""
        gamer_mode_enabled = (index == 0)
        
        self.logger.info("Modo Gamer alterado", service="Configuration", additional_data={"enabled": gamer_mode_enabled})
        
        from back_firewall import AdvancedFirewall
        firewall = AdvancedFirewall()
        firewall.set_gamer_mode(gamer_mode_enabled)
        
        if gamer_mode_enabled:
            QMessageBox.information(None, "Modo Gamer", "Modo Gamer ativado!\nAnálise de IA desligada para melhor desempenho.")
        else:
            QMessageBox.information(None, "Modo Gamer", "Modo Gamer desativado.\nAnálise de IA religada.")

    def change_operation_mode(self, index):
        """Altera o modo de operação"""
        modes = ["Automático", "Interativo", "Personalizado"]
        self.logger.info("Modo de operação alterado", service="Configuration", additional_data={
            "new_mode": modes[index]
        })
    
    def change_network_profile(self, index):
        """Altera o perfil de rede"""
        profiles = ["Público", "Privado", "Domínio"]
        self.logger.info("Perfil de rede alterado", service="Configuration", additional_data={
            "new_profile": profiles[index]
        })
    
    def update_ia_config(self):
        """Atualiza a configuração de IA"""
        config = {
            "BruteForce": self.ui.checkBox_BruteForce.isChecked(),
            "AcessoRemoto": self.ui.checkBox_AcessoRemoto.isChecked(),
            "PortScan": self.ui.checkBox_PortScan.isChecked(),
            "DDoS": self.ui.checkBox_DDOS.isChecked()
        }
        self.logger.info("Configuração de IA atualizada", service="AI Configuration", additional_data=config)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setQuitOnLastWindowClosed(False)
    
    window = FirewallApp()
    window.show()
    
    sys.exit(app.exec())