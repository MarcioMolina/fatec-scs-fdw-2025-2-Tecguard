from win10toast import ToastNotifier

notifier = ToastNotifier()
notifier.show_toast(
    "Título da Notificação",
    "Este é o corpo da mensagem",
    duration=5  # duração em segundos
)