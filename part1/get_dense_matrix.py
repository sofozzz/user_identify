def get_dense_matrix(matrix):
    '''
     Создает разряженную матрицу в которой строкам будут соответствовать сессии из 10 сайтов, а столбцам – индексы сайтов.
     На пересечении строки ii и столбца jj будет стоять число nijnij – сколько раз сайт jj встретился в сессии номер ii.
     Возвращает разряженную матрицу.
    '''
    site_ids = set(element for row in matrix for element in row if element != 0) # создаем список id сайтов
    
    i = 0
    data = []
    col = []
    rows = []

    for row in tqdm(matrix):
        
        unique, counts = np.unique(row, return_counts=True)
        
        temp_dict = dict(zip(unique, counts))
        
        for k in temp_dict:
            if k == 0:
                continue
            
            data.append(temp_dict[k])
            rows.append(i)
            col.append(k-1)
            
        i += 1
        
    X_sparse = csr_matrix((data, (rows, col)), shape=(matrix.shape[0], len(site_ids)))
    
    return X_sparse