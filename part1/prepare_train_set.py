def prepare_train_set(path_to_csv_files, session_length=10):
    '''
    Принимает на вход путь к каталогу с csv-файлами path_to_csv_files и параметр session_length. Каждый файл имеет в название user_id
    и содержит список посещенных сайтов, с указанием времени начала.
    Возвращает DataFrame, в котором строки соответствуют уникальным сессиям из session_length сайтов, session_length столбцов – индексам этих session_length сайтов
    и последний столбец – ID пользователя и частотный словарь сайтов вида {'site_string': [site_id, site_freq]}.
    '''
    site_freq = {} # создаем пустой словарь
    
    list_sessions = []

    for userfile in tqdm(glob(os.path.join(path_to_csv_files, '*.csv'))): # обходим все файлы в каталоге с расшарением .csv

        sites = pd.read_csv(userfile).site.values # читаем названия сайтов из файла
        
        for site in sites:
            if site not in site_freq: # проверяем наличие сайта в частотном словаре
                site_freq[site] = [len(site_freq) + 1, 0] # если такого сайта еще нет в словраре, то создаем такой элемент
            site_freq[site][1] +=1 # увеличиваем счетчик частоты повторений сайта 
        
        
        count_session = len(sites)//session_length if len(sites)%session_length == 0 else len(sites)//session_length+1

        for sindex in range(count_session):
            sessions = []
            for index in range(sindex * session_length, sindex * session_length + session_length):
                if index < len(sites):
                    sessions.append(site_freq[sites[index]][0])
                else:
                    sessions.append(0)
            sessions.append(get_user_id(userfile))
            list_sessions.append(sessions)
    
    
    headers = ['site' + str(index) for index in range(1, session_length+1)] + ['user_id'] # создаем список с заговолками для столбцов DataFrame
    train_data = pd.DataFrame(data=list_sessions, columns=headers) # создаем DataFrame
    
    return train_data, site_freq
