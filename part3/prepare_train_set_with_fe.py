def prepare_train_set_with_fe(path_to_csv_files, site_freq_path, feature_names, session_length=10, window_size=10):
    '''
    Создайте на основе функций prepare_train_set и prepare_sparse_train_set_window новую – prepare_train_set_with_fe, (от "feature engineering"), создайте следующие признаки:

    session_timespan – продолжительность сессии (разница между максимальным и минимальным временем посещения сайтов в сессии, в секундах)
    #unique_sites – число уникальных сайтов в сессии
    start_hour – час начала сессии (то есть час в записи минимального timestamp среди десяти)
    day_of_week – день недели (то есть день недели в записи минимального timestamp среди десяти)

    Функция должна возвращать новый DataFrame (как возвращала функция prepare_train_set),
    только признаков должно быть на 4 больше. Порядок, в котором добавляются признаки: site1, ... site10, session_timespan, #unique_sites, start_hour, day_of_week и user_id (это видно и чуть ниже по тому, как функция вызывается).
    '''

    with(open(site_freq_path, 'rb')) as file:
        site_freq = pickle.load(file)
    
    list_sessions = []
    
    for filename in tqdm(glob(os.path.join(path_to_csv_files, '*.csv'))):
        times = pd.read_csv(filename, parse_dates=['timestamp']).timestamp
        sites = pd.read_csv(filename).site.values
        
        count_sessions = len(sites) // window_size if len(sites) % window_size == 0 else len(sites) // window_size + 1
        
        for sindex in range(count_sessions):
            have_zero = 0
            count_sites = 0
            sessions = []
            for index in range(sindex * window_size, sindex * window_size + session_length):
                if index < len(sites):
                    sessions.append(site_freq[sites[index]][0])
                    count_sites += 1
                else:
                    have_zero = 1
                    sessions.append(0)
                    
                    
            unique_sites = len(set(sessions)) - have_zero
            session_timespan = (times[sindex * window_size + (count_sites - 1)] - times[sindex * window_size]).seconds
            sessions.append(session_timespan)
            sessions.append(unique_sites)
            start_hour = times[sindex * window_size].hour
            sessions.append(start_hour)
            day_of_week = times[sindex * window_size].dayofweek
            sessions.append(day_of_week)
            sessions.append(get_user_id(filename))
            list_sessions.append(sessions)
    
    return pd.DataFrame(list_sessions, columns=feature_names)