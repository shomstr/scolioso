BOT_INFO = (
    "🤖 Bot information: \n\n"
    "🐍 <b>Python: {python} </b> \n"
    "🗂 <b>Aiogram: {aiogram} </b> \n "
    "📟 <b>CPU: {process_cpu_percent}% </b> \n"
    "📟 <b>RAM: {process_ram} MB ({process_ram_percent}%) </b> \n"
    "🚀 <b>Bot working: <code>{bot_working}</code> </b> \n\n"
    "📊 Server information: \n\n"
    "📟 <b>CPU: {cpu} ядер(-ро) {cpu_load}% </b> \n"
    "📟 <b>RAM: {ram} / {ram_load_mb}MB ({ram_load}%) </b> \n"
    "💻 <b>Arch: {arch} </b> \n"
    "💿 <b>OS: {os} </b> \n\n"
    "👥 <b>All users in db: {users_in_db}</b> \n"
)

BAG_TEXT = (
    "<b>🍏 Ваше дерево/Дерево пользователя</b> \n\n"
    "<b>🍃 Лепестки</b> <code>{user.petals}</code> <b>💧Вода</b> <code>{user.water}</code> \n"
    "<b>🍂 Листвы</b> <code>0</code> \n"
    "<b>❇️ Прогул</b> <code>0</code> \n"
)

WALK_TEXTS = [
    " 🌳 Ваша прогулка принесла удачу! Вы нашли {petals} лепестка ☘️ и {water} бутылки воды 💧",
    " 🍃 Здорово! Вам попались {petals} лепестка ☘️ и {water} бутылки воды 💧",
    " 🌿 Отлично! На пути вы обнаружили {petals} лепестков ☘️ и {water} бутылки воды 💧",
    " 🌼 Ура! Вы нашли {petals} лепестка ☘️ и {water} бутылки воды 💧",
    " 🌱 Прекрасная прогулка! Вам удалось собрать {petals} ☘️ лепестков и {water} бутылки воды 💧",
    "🌳 Прекрасно! Вы наткнулись на {petals} лепестков ☘️ и {water} бутылки воды 💧"
    "🍂 Вам повезло! Вы нашли {petals} лепестка ☘️ и {water} бутылки воды 💧"
    "🌸 Успех! На вашем пути оказались {petals} ☘️ лепестков и {water} бутылки воды 💧"
    "🌾 Отлично! Вы обнаружили {petals} лепестка ☘️ и {water} бутылки воды💧"
    "🌼 Замечательно! Вам удалось собрать {petals} ☘️ лепестков и {water} бутылки воды 💧",
]
