rule http_attack {
    strings:
        $cmd = /cmd\.exe[\s\/\\-]/ nocase
        $powershell = /powershell\s+-[eencod]/ nocase
    condition:
        any of them
}

rule sql_injection {
    strings:
        $union = "union select" nocase
        $or_1eq1 = "or 1=1" nocase
    condition:
        any of them
}