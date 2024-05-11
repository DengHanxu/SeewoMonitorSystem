from psutil import process_iter

def check_process(process_name):
    processes = process_iter()
    if type(process_name) == str:
        process_name = process_name.lower()
        for process in processes:
            if process.name().lower() == process_name :
                return True
        return False
    elif type(process_name) == list:
        for i in range(len(process_name)):
            process_name[i] = process_name[i].lower()
        for process in processes:
            if process.name().lower() in process_name :
                return True
        return False
    else:
        raise TypeError('参数必须为 str 或 list')

if __name__ == '__main__':
    while True:
        try:
            print(check_process(input('Process name >>>')))
        except Exception as e:
            print(e)

