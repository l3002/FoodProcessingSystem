import mysql.connector as sql
import tabulate
try:
    p=input('Enter the password of your mysql: ')
    conn=sql.connect(host="localhost", user="root", passwd=p)
    if conn.is_connected():
        print("Connected Sucessfully")
        c1= conn.cursor()
        c1.execute('show databases')
        d=c1.fetchall()
        if ('food',) not in d:
            c1.execute('create database food')
        c1.execute('use food')
        c1.execute('show tables')
        data=c1.fetchall()
        if ('myc',) not in data:
            c1.execute('create table myc(account_no int(8) primary key not null,cname varchar(20),address varchar(50))')
            print('Customer Tables Created')
        if ('sales',) not in data:
            c1.execute('create table sales(fname varchar(20),price float(10),address varchar(50),account_no int(8),date_time timestamp default current_timestamp)')
            print('Sales Tables Created')
    print()
    def create(ano):
        v_cust_name=input("Enter the customer's name:")
        v_address=input("Enter the customer's address:")
        v_SQL_insert="insert into myc values('"+ano+"','"+v_cust_name+"','"+v_address+"')"
        c1.execute(v_SQL_insert)
        conn.commit()
        print("ACCOUNT CREATED")
        x=input('Would you like to log in to the account(Y/N): ')
        if x.upper()=='Y':
            login(ano)
        else:
            print()
            print('                  THANK YOU')
    def login(ano):
        c2=0
        c1=conn.cursor()
        c1.execute('select * from myc')
        data=c1.fetchall()
        if data==[]:
            print('NO ACCOUNT HAS BEEN MADE YET!')
            x=input('Would you like to create one(Y/N):')
            if x.upper()=='N':
                print()
                print('                      THANK YOU')
            else:
                create(ano)
        for row in data:
            if (int(ano) in row):
                print("You've logged in as ",end="")
                c1=conn.cursor()
                c1.execute("select cname from myc where account_no='"+ano+"'")
                data=c1.fetchall()
                for i in data:
                    for j in i:
                        print(j)
                while True:
                    if (c2==5):
                        print()
                        print('                  THANK YOU')
                        break
                    print()
                    print('                        OPERATION MENU')
                    print('1. TO SEE DETAILS')
                    print('2. TO UPDATE DETAILS')
                    print('3. TO ORDER FOOD')
                    print('4. TO SEE ORDERED FOOD')
                    print('5. TO EXIT')
                    c2=int(input('Enter your choice: '))
                    if (c2==5):
                        print()
                        print('                  THANK YOU')
                        break
                    if (c2==1):
                        c1=conn.cursor()
                        c1.execute("select * from myc where account_no='"+ano+"'")
                        data=c1.fetchall()
                        print('THE DETAIL OF CUSTOMERS')
                        print(tabulate.tabulate(data,headers=['Account no','Name','Address'],tablefmt='fancy_grid'))
                    elif (c2==2):
                        print('TO UPDATE FILL THIS')
                        c1=conn.cursor()
                        update_show="select * from myc where account_no='"+ano+"'"
                        c1.execute(update_show)
                        data=c1.fetchall()
                        print(tabulate.tabulate(data,headers=['Account no','Name','Address'],tablefmt='fancy_grid'))
                        while True:
                            print('CHOOSE THE DETAIL TO BE CHANGED')
                            print('1. NAME')
                            print('2. ADDRESS')
                            a=int(input('Enter your choice: '))
                            if a==1:
                                n=input('Enter the new name: ')
                                c1.execute("update myc set cname='"+n+"' where account_no='"+ano+"'")
                            elif a==2:
                                n=input('Enter the new address: ')
                                c1.execute("update myc set address='"+n+"' where account_no='"+ano+"'")
                            print('YOUR DETAILS ARE SUCESSFULLY UPDATED')
                            print('AFTER UPDATION:')
                            update_show="select * from myc where account_no='"+ano+"'"
                            c1.execute(update_show)
                            data=c1.fetchall()
                            print(tabulate.tabulate(data,headers=['Account no','Name','Address'],tablefmt='fancy_grid'))
                            x=input('Would you like to update more(Y/N): ')
                            if x.upper()=='N':
                                break
                    elif(c2==3):
                        m=['FOOD MENU']
                        data=[['BURGER','Rs. 50'],['PIZZA','Rs. 90'],['MAC & CHEESE','Rs. 70'],['TACO','Rs. 50'],['PUDDING','Rs. 30'],['HOT CHOCOLATE','Rs. 100']]
                        print(tabulate.tabulate(data,headers=m,tablefmt='fancy_grid'))
                        while True:
                            v_f_name=input("Enter the name of food: ")
                            v_price=input("Enter the cost of the food: ")
                            v_address=input("Enter the address: ")
                            v_SQL_insert="insert into sales(fname,price,address,account_no) values('"+ v_f_name+"','"+v_price+"','"+v_address+"','"+ano+"')"
                            c1.execute(v_SQL_insert)
                            conn.commit()
                            print("SUCESSFULLY ORDERED")
                            x=input('Would you like to order anything else(Y/N): ')
                            if x.upper()=='N':
                                break
                    elif(c2==4):
                        c1=conn.cursor()
                        c1.execute("select fname,price,sales.address,date_time from sales,myc where sales.account_no=myc.account_no and myc.account_no='"+ano+"'")
                        data=c1.fetchall()
                        print('THE DETAIL OF ORDERED FOOD')
                        print(tabulate.tabulate(data,headers=['Account no','Name','Address','Datetime'],tablefmt='fancy_grid'))
                    x=input('Would you like to use operation menu again(Y/N): ')
                    if x.upper()=='N':
                        c2=5
        if c2!=5:
            print('Account no not found')
            x=input('Would you like to make an account with this account no(Y/N): ')
            if x.upper()=='N':
                print()
                print('                   THANK YOU')
            else:
                create(ano)
    print("                    ORDER YOUR FOOD HERE")
    c1=conn.cursor()
    print("1.CREATE YOUR ACCOUNT")
    print("2.LOG IN")
    choice=int(input("ENTER YOUR CHOICE:"))
    if choice ==1:
        v_account_no=input("Enter the account number:")
        create(v_account_no)
    if choice==2:
        print('TO LOGIN FILL THIS DETAIL')
        v_account_no=input('Enter the account no:')
        login(v_account_no)
except sql.errors.ProgrammingError:
    print()
    print('                          XX ACCESS DENIED XX')
