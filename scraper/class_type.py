import pandas as pd
from scraper.common.dbconn import DBConn
import os

FUND_DB = os.getenv('FUND_DB_URI')


def fetch_product_info():
    query = """
        select ticker, product_name, trait_division
        from fund_kofia.product_info_practice
        where trait_division like '%CLASS%' 
    """
    return DBConn(FUND_DB).fetch(query).df()


def last_few_words(class_type):
    df = fetch_product_info()
    funds = df['product_name'].tolist()
    class_list = []
    for i in funds:
        if class_type == 'S':
            last_words = i[-7:]
            # USD, ELS S-P, S-T, 등등 잡히는 문제 있다.
            # S-P, S-T는 덮어 씌우는 것으로 문제해결 가능할듯
            if last_words.find('S') != -1 or last_words.find('s') != -1:
                class_list.append([i, 'class_S'])
        elif class_type == 'C':
            last_words = i[-7:]
            # Class에 있는 C까지 포함되는 문제가 있다.
            if last_words.find('C') != -1:
                class_list.append([i, 'class_C'])
        elif class_type == 'A':
            last_words = i[-7:]
            if last_words.find('A') != -1:
                class_list.append([i, 'class_A'])
        elif class_type == 'B':
            last_words = i[-3:]
            if last_words.find('B') != -1:
                class_list.append([i, 'class_B'])
        elif class_type == 'D':
            # last_words = i[-7:]
            # USD의 D가 잡히는 문제가 있다.
            last_words = i[-4:]
            if last_words.find('D') != -1:
                class_list.append([i, 'class_D'])
        elif class_type == 'E':
            last_words = i[-6:]
            # ELE, (E)(주식)인 펀드들이 섞이는 문제가 있다.
            if last_words.find('E') != -1 or last_words.find('e') != -1:
                class_list.append([i, 'class_E'])
        elif class_type == 'F':
            last_words = i[-4:]
            # MMF의 F가 잡히는 문제가 있다.
            if last_words.find('F') != -1 or last_words.find('f') != -1:
                class_list.append([i, 'class_F'])
        elif class_type == 'H':
            last_words = i[-3:]
            # H, UH 환헷지 표시가 잡히는 문제가 있다.
            if last_words.find('H') != -1:
                class_list.append([i, 'class_H'])
        elif class_type == 'I':
            last_words = i[-5:]
            if last_words.find('I') != -1 or last_words.find('i') != -1:
                class_list.append([i, 'class_I'])
        elif class_type == 'P':
            last_words = i[-11:]
            if last_words.find('P') != -1 or last_words.find('p') != -1 or last_words.find(
                    'R') != -1 or last_words.find('r') != -1 or last_words.find('퇴직') != -1:
                class_list.append([i, 'class_P'])
        elif class_type == 'W':
            last_words = i[-6:]
            # 마이다스블루칩배당증권투자신탁W(주식)S 하나가 잡히는 문제가 있다.
            if last_words.find('W') != -1 or last_words.find('w') != -1:
                class_list.append([i, 'class_W'])
        elif class_type == 'J':
            last_words = i[-3:]
            # 한국투자신종법인용MMF 15CMJ의 클래스가 C인지 J인지...
            if last_words.find('J') != -1:
                class_list.append([i, 'class_J'])
        elif class_type == 'S-P':
            last_words = i[-10:]
            if last_words.find('S-P') != -1 or last_words.find('S-R') != -1:
                class_list.append([i, 'class_S-P'])
        elif class_type == 'S-T':
            last_words = i[-6:]
            if last_words.find('S-T') != -1:
                class_list.append([i, 'class_S-T'])
        elif class_type == 'G':
            last_words = i[-6:]
            if last_words.find('G') != -1 or last_words.find('g') != -1:
                class_list.append([i, 'class_G'])

    class_type = pd.DataFrame(class_list)
    return class_type


def main(classes):
    class_funds = []
    for i in classes:
        class_type = last_few_words(i)
        class_funds.append(class_type)
    df = pd.concat(class_funds)
    df.columns = ['product_name', 'class_type']
    df = df.drop_duplicates(subset='product_name', keep='last')
    return df


if __name__ == '__main__':
    classes = ['S', 'C', 'A', 'B', 'D', 'E', 'F', 'H', 'I', 'P', 'W', 'J', 'S-P', 'S-T', 'G']
    class_type = main(classes)
    sd = 0
