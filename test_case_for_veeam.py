import subprocess
import re
import time
import json
import os
def command_cpu(name):
    command = '''
    function Get-CPUPercent
    {
        $CPUPercent = @{
            Name = 'CPUPercent'
            Expression = {
            $TotalSec = (New-TimeSpan -Start $_.StartTime).TotalSeconds
            [Math]::Round( ($_.CPU * 100 / $TotalSec), 2)
            }
        }
        Get-Process -Name %s| Select-Object -Property Name, 
        $CPUPercent, WorkingSet, Handle, 
        PrivateMemorySize| Sort-Object -Property CPUPercent -Descending  
    }
    Get-CPUPercent
    '''%name
    return command

def inp():
    abs_path = input('Введите путь до исполняемого файла(.exe):')
    path, filename = os.path.split(abs_path)
    filename = filename[:-4]
    while True:    
        period = float(input('Введите период опроса, с(>=1):'))
        if period >= 1:
            break
        else:
            print('Вы ввели неверное значение, придётся ввести заново')
    return filename, period, path

def one_time_data(name, period):
    args_cpu = ["powershell", command_cpu(name), 'Get-CPUPercent']
    process_cpu = subprocess.Popen(args_cpu, stdout=subprocess.PIPE)
    data = process_cpu.communicate()
    out = {'CPUPercent': 0,'WorkingSet': 0, 'Handle': 0, 'PrivateMemorySize': 0}
    line = data[0].decode().split()
    for _i in range(len(line)):
        if line[_i] in out:
            try:
                out[line[_i]] += float(line[_i + 2].replace(',', '.'))
            except ValueError:
                continue
    return out

def format_one_time_data(data):
    for _i in data:
        if _i != 'CPUPercent':
            data[_i] = int(data[_i])
        else:
            data[_i] = float('{:.2f}'.format(data[_i]))

def time_line(name, period):
    start_time = time.time()
    out = one_time_data(name, period)
    format_one_time_data(out)
    stop_time = time.time()
    delta_time = stop_time - start_time
    if delta_time > period:
        seconds = time.time()
        date = time.ctime(seconds).split()
    else:
        seconds = start_time + period
        date = time.ctime(seconds).split()        
        time.sleep(period - delta_time)
        
    date = {'Year': date[-1], 'Month':date[1], 'Day': date[2], 'Time': date[3]}
    out['CurrentTime'] = date
    out['TotalSec'] = int(seconds)
    out['Name'] = name
    return out
    

    
if __name__ == '__main__':
    name, period, path = inp()
    save_to_json = []
    with subprocess.Popen([name]) as proc:
        while subprocess.Popen.poll(proc) is None:
            data = time_line(name, period)
            save_to_json.append(data)
            for _i in data:
                print(_i + ':', data[_i])
            print()
    absFilePath = os.path.abspath(__file__)
    path, _ = os.path.split(absFilePath)
    os.chdir(path)
    print(os.getcwd()) 
    with open("resource_data_file.json", "a") as write_file:
        json.dump(save_to_json, write_file)
    