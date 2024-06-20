from utils import bot, client, InlineKeyboardButton, InlineKeyboardMarkup

def get_button_handler(call, data_names):
    pages = int(call.data.split(':')[-4])
    num = int(call.data.split(':')[-2])
    action = call.data.split(':')[-1]
    query_or_artist_id = call.data.split(':')[-3]

    global fake_page
    # start_index = num * 10
    if action == 'next':
        page = num + 1
        fake_page = page + 1
    elif action == 'prev':
        page = num - 1
        fake_page = page + 1
    elif action == 'null':
        page = num
        bot.answer_callback_query(call.id, text='Это просто показатель страницы!')
        return

    keyboard = []
    start_index = page * 10

    if data_names == ('get_button_artist', 'artist_info'):
        query = query_or_artist_id
        for i in range(page, pages):
            wasd = client.search(text=f'{query}', type_='artist', page=page)
            if i == page:
                for artist in wasd.artists.results[:10]:
                    button = InlineKeyboardButton(text=artist.name, callback_data=f'{data_names[1]}:{artist.id}')
                    keyboard.append([button])

    elif data_names == ('get_button_album', 'get_album_tracks'):
        artist_id = query_or_artist_id
        artist_info = client.artists_direct_albums(artist_id, page_size= 200)
        for album in artist_info[start_index:start_index+10]:
            button = InlineKeyboardButton(text=album.title, callback_data=f'{data_names[1]}:{album.id}')
            keyboard.append([button])

    elif data_names == ('get_button_track', 'download_track', 'get_artist_albums'):
        album_id = query_or_artist_id
        info = client.albums_with_tracks(album_id)
        artist_id = info.artists[0].id
        artist_info = client.artists(artist_id)
        album_count = artist_info[0].counts.direct_albums
        tracks = []
        for i, volume in enumerate(info.volumes):
            if len(info.volumes) > 1:
                tracks.append(f'{i + 1}')
            tracks += volume
        for track in tracks[start_index:start_index+10]:
            button = InlineKeyboardButton(text=track.title, callback_data=f'{data_names[1]}:{track.id}:{album_id}')
            keyboard.append([button])

    page_button = (InlineKeyboardButton(f'Страница {fake_page}/{pages}', callback_data=f'{data_names[0]}:{pages}:{query_or_artist_id}:{page}:null'))
    if page < pages - 1:
        next_button = (InlineKeyboardButton(text=f'Вперёд', callback_data=f'{data_names[0]}:{pages}:{query_or_artist_id}:{page}:next'))
        keyboard.append([page_button, next_button])
        if page > 0:
            back_button = (InlineKeyboardButton(text=f'Назад', callback_data=f'{data_names[0]}:{pages}:{query_or_artist_id}:{page}:prev'))
            keyboard[-1].insert(0, back_button)
    else:
        keyboard.append([page_button])
        if page > 0:
            back_button = (InlineKeyboardButton(text=f'Назад', callback_data=f'{data_names[0]}:{pages}:{query_or_artist_id}:{page}:prev'))
            keyboard[-1].insert(0, back_button)

    if data_names == ('get_button_track', 'download_track','get_artist_albums'):
        back_button = InlineKeyboardButton(text="Вернуться к альбомам",
                                           callback_data=f'{data_names[2]}:{artist_id}:{album_count}')
        keyboard.append([back_button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)