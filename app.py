import csv
import re
import requests


def read_csv(filename):
    result = []
    with open(filename, newline='', encoding='utf8') as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            if index == 0:
                continue
            result.append(row)
    return result


def write_csv(filename, result): 
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for item in result:
            writer.writerow(item)


def request_for_mobile(phone_num):
    url = "https://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel=" + phone_num
    res = requests.get(url)
    result = res.text
    print(result)
    return re.search('province\:\'(\w+)\'', result).group(1)


def query_mobile(result):
    data = []
    for index, ele in enumerate(result):
        if index == 0:
            continue
        # elif index > 10000:
        #     break
        if ele[0][0:7] != result[index - 1][0][0:7]:
            mobile = ele[0]
            province = request_for_mobile(mobile)
            data.append([mobile, province])
        else:
            data.append([mobile,])
        if index % 10000 == 0:
            write_csv('result' + str(index) + '.csv', data)
            data = []
    return data

        
def run():
    csv_file = 'mobile_phone.csv'
    result = read_csv(csv_file)
    csv_result = query_mobile(result)
    # write_csv('result.csv', csv_result)
    


if __name__ == "__main__":
    run()
