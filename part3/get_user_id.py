def get_user_id(filename):
    '''Получает ID пользователя из названия файла. Возвращает целое число.'''
    
    extension = '.csv'
    len_number = 4
    end = filename.find(extension)
    start = end - len_number
    
    return int(filename[start:end])