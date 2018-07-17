def prepare_sparse_train_set_window(path_to_csv_files, site_freq_path, session_length=10, window_size=10):
    '''
    Создает разреженную матрицу X_sparse (двухмерная Scipy.sparse.csr_matrix), в которой строки соответствуют сессиям из session_length сайтов, а max(site_id) столбцов – количеству посещений site_id в сессии.
     и вектор y (Numpy array) "ответов" в виде ID пользователей, которым принадлежат сессии из X_sparse.
    Возвращает матрицу и вектор.
    '''
    with (open(site_freq_path, 'rb')) as file:
        site_freq = pickle.load(file)
        
    user_id = 1

    users = []
    rows = []
    
    for userfile in tqdm(glob(os.path.join(path_to_csv_files, '*.csv'))):
        list_sessions = []

        sites = pd.read_csv(userfile).site.values
        count_session = len(sites)//window_size if len(sites)%window_size == 0 else len(sites)//window_size+1
        for sindex in range(count_session):
            sessions = []
            for index in range(sindex * window_size, sindex * window_size + session_length):
                if index < len(sites):
                    sessions.append(site_freq[sites[index]][0])
                else:
                    sessions.append(0)
            list_sessions.append(sessions)
        
        users.extend([user_id] * len(list_sessions))
        rows.extend(list_sessions)
    
        user_id = user_id + 1
    return get_dense_matrix(np.array(rows)), users