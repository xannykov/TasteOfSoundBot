from utils import bot, client, InlineKeyboardMarkup, InlineKeyboardButton, types, io, requests
from get_button import get_button_handler



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет!""\N{slightly smiling face}"
    "\nЯ бот, который ищет музыкальных исполнителей по твоему запросу."
    "\nНужен я больше для справочной информации об исполнителях и их работах.""\N{winking face}"
    "\nЧтобы начать пользоваться напиши любого интересующего тебя исполнителя.")



@bot.message_handler(content_types=['text'])
def send_search_request(message):
    query = message.text
    search_result = client.search(query, type_='artist')

    if search_result.artists:
        text = [f'Результаты по запросу "{query}":', f'\nНайдено исполнителей: {search_result.artists.total}']
        pages = int((search_result.artists.total - 1) / 10) + 1

        keyboard = []

        wasd = client.search(text=f'{query}', type_='artist')

        for artist in wasd.artists.results[:10]:
            button = InlineKeyboardButton(text=artist.name, callback_data=f'artist_info:{artist.id}')
            keyboard.append([button])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if pages > 1:
            current_page = 1
            real_page = 0
            next_button = InlineKeyboardButton(text=f'Вперёд', callback_data=f'get_button_artist:{pages}:{query}:{real_page}:next')
            page_button = InlineKeyboardButton(text=f'Страница {current_page}/{pages}',
                                               callback_data=f'get_button_artist:{pages}:{query}:{real_page}:null')
            keyboard.append([page_button, next_button])

        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.send_message(message.chat.id, '\n'.join(text), reply_markup=reply_markup)
    else:
        bot.send_message(message.chat.id, 'Не удалось найти исполнителя.')



@bot.callback_query_handler(func=lambda call: call.data.startswith('get_button_artist'))
def callback_artists_handler(call: types.CallbackQuery):
    get_button_handler(call, ('get_button_artist', 'artist_info'))



@bot.callback_query_handler(func=lambda call: call.data.startswith('artist_info'))
def send_artist_info(call: types.CallbackQuery):
    artist_id = call.data.split(':')[-1]
    artist_info = client.artists(artist_id)
    info = client.artists_brief_info(artist_id)

    description = info.artist.hand_made_description
    if description is None:
        description = ''

    name = artist_info[0].name
    image = artist_info[0].cover.uri
    genre = ', '.join(artist_info[0].genres)
    count_albums = artist_info[0].counts.direct_albums
    count_tracks = artist_info[0].counts.tracks

    if name:
        message_text = f'Исполнитель: {name}\nЖанр: {genre}\nПесен: {count_tracks}\nАльбомов: {count_albums} \n\n{description}'
        keyboard_alb = types.InlineKeyboardMarkup()
        keyboard_alb.add(types.InlineKeyboardButton(text='Альбомы', callback_data=f'get_artist_albums:{artist_id}:{count_albums}'))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup={})
        if image:
            bot.send_photo(chat_id=call.message.chat.id, photo=image.replace("%%", "800x800"), caption=message_text, reply_markup=keyboard_alb)
        else:
            bot.send_message(chat_id=call.message.chat.id, text=message_text, reply_mrkup=keyboard_alb)
    else:
        bot.send_message(chat_id=call.message.chat.id, text='Не удалось получить информацию об исполнителе.')



@bot.callback_query_handler(func=lambda call: call.data.startswith('get_artist_albums'))
def send_album_info(call: types.CallbackQuery):
    count_albums = int(call.data.split(":")[-1])
    artist_id = call.data.split(":")[-2]
    pages = int((count_albums - 1) / 10) + 1

    keyboard = []

    artist_info = client.artists_direct_albums(artist_id)
    for album in artist_info[:10]:
        button = InlineKeyboardButton(text = album.title, callback_data=f'get_album_tracks:{album.id}')
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if pages > 1:
        current_page = 1
        real_page = 0
        next_button = InlineKeyboardButton(text=f'Вперёд', callback_data=f'get_button_album:{pages}:{artist_id}:{real_page}:next')
        page_button = InlineKeyboardButton(text=f'Страница {current_page}/{pages}',
                                           callback_data=f'get_button_album:{pages}:{artist_id}:{real_page}:null')

        keyboard.append([page_button, next_button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('get_button_album'))
def callback_album_handler(call: types.CallbackQuery):
    get_button_handler(call, ('get_button_album', 'get_album_tracks'))



@bot.callback_query_handler(func=lambda call: call.data.startswith('get_album_tracks'))
def callback_track_handler(call: types.CallbackQuery):
    album_id = call.data.split(':')[-1]
    info = client.albums_with_tracks(album_id)

    artist_id = info.artists[0].id
    artist_info = client.artists(artist_id)
    album_count = artist_info[0].counts.direct_albums
    track_count = info.track_count

    keyboard = []
    pages = int((track_count - 1) / 10) + 1
    tracks = []
    for i, volume in enumerate(info.volumes):
        if len(info.volumes) > 1:
            tracks.append(f'{i + 1}')
        tracks += volume

    for track in tracks[:10]:
        button = InlineKeyboardButton(text=track.title, callback_data=f'download_track:{track.id}:{album_id}')
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)

    current_page = 1
    real_page = 0
    if pages > 1:
        next_button = InlineKeyboardButton(text=f'Вперёд', callback_data=f'get_button_track:{pages}:{album_id}:{real_page}:next')
        page_button = InlineKeyboardButton(text=f'Страница {current_page}/{pages}',
                                           callback_data=f'get_button_track:{pages}:{album_id}:{real_page}:null')
        keyboard.append([page_button, next_button])
    else:
        page_button = InlineKeyboardButton(text=f'Страница {current_page}/{pages}',
                                           callback_data=f'get_button_track:{pages}:{album_id}:{real_page}:null')

        keyboard.append([page_button])
    reply_markup = InlineKeyboardMarkup(keyboard)

    back_button = InlineKeyboardButton(text="Вернуться к альбомам", callback_data=f'get_artist_albums:{artist_id}:{album_count}')
    keyboard.append([back_button])
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('get_button_track'))
def callback_album_handler(call: types.CallbackQuery):
    get_button_handler(call, ('get_button_track', 'download_track', 'get_artist_albums'))



@bot.callback_query_handler(func=lambda call: call.data.startswith('download_track'))
def callback_album_handler(call: types.CallbackQuery):
    wait_message = bot.send_message(call.message.chat.id, "Подождите пару секунд...")
    album_id = call.data.split(':')[-1]
    track_id = call.data.split(':')[-2]
    track = client.tracks(track_id)[0]
    download_info = client.tracksDownloadInfo(track_id)
    download_url = download_info[0].getDirectLink()
    cover_url = track.getCoverUrl()
    cover_image = requests.get(cover_url).content
    response = requests.get(download_url, stream=True)
    audio = io.BytesIO(response.content)
    bot.send_audio(call.message.chat.id, audio, title=track.title, performer=track.artists[0].name, thumb=cover_image)
    bot.delete_message(call.message.chat.id, wait_message.message_id)



bot.polling(non_stop=True)


