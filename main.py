from flask import Flask , render_template, request,redirect, url_for, flash
from connection import connection_database, execute_data, execute_data_insert
import requests

app = Flask(__name__, template_folder="template")

@app.route("/home", methods=['GET', 'POST'])
def home():

    url = "https://notify-api.line.me/api/notify"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": "Bearer 7lVpHVzPrquKZ3M4aucCt7SBuXj5tMfw8oWuQSqQTWx"
    }

    order_text = ""
    stock_text = ""
    stock_textgrp = ""
    customer_text = ""
    customergrp_text = ""
    select = ""

    cus_name_old = []
    cus_prefix_old = []
    cus_tel_old = []
    pro_name_old = []

    button_serch = None
    button_add = None
    button_edit = None
    button_delete = None
    button_select_edit = None
    search_tb_button = None
    search_tb_text = None
    
    result = connection_database()

    if result > 0:
        
        search_tb_text = request.form.get("search_tb_text")
        query = "SELECT * FROM tbSae"
        order_text = execute_data(query)
        
        select_stock = request.form.get("stock")
        select_value = request.form.get("customer")
        custcode = select_value

        query = "SELECT * FROM tbCustomer"
        result_customer = execute_data(query)
        customer_text = result_customer

        query = "SELECT * FROM tbStock"
        result_stock = execute_data(query)
        stock_text = result_stock
        
        query = "SELECT * FROM tbStockGrp"
        result_stockgrp = execute_data(query)
        stock_textgrp = result_stockgrp

        if select_value == "":
            select_value = None

        if 'button_serch' in request.form:
            print("ค้นหา", select_value)

            if select_value is not None:

                for row in customer_text:
                    if select_value == row[0]:
                        customergrp_text = row[1]

                query = "SELECT CustGrpName FROM tbCustomerGrp where CustGrpCode = '" + customergrp_text + "'"
                result_customergrp = execute_data(query)
                
                for result_text in result_customergrp:
                    customergrp_text = result_text[0]
            else:
                print("Select value is None")

        if 'search_tb_button' in request.form:
            search_tb_button = request.form.get("search_tb_text")
            print("Search Text",search_tb_text)

            try:
                # ลองค้นหาจาก SOCode ก่อน
                query = f"SELECT * FROM tbSae WHERE SOCode = '{search_tb_button}'"
                order_text = execute_data(query)
                
                if not order_text:
                    raise ValueError("No data found")  # บังคับให้ไปทำ except

            except Exception as e:
                print(f"Error SOCode: {e}")
                
                try:
                    query = f"SELECT StockCode FROM tbStock WHERE StockName LIKE '%{search_tb_button}%'"
                    text = execute_data(query)
                    print(text)
                    
                    if text:
                        result = text[0][0]
                        query = f"SELECT * FROM tbSae WHERE StockCode = '{result}'"
                        order_text = execute_data(query)

                    if not order_text:
                        raise ValueError("No data found in Stock")

                except Exception as e:
                    print(f"Error Stock: {e}")

                    try:
                        query = f"SELECT CustCode FROM tbCustomer WHERE CustName LIKE '%{search_tb_button}%'"
                        text = execute_data(query)
                        print(text)

                        if text:
                            result = text[0][0]
                            query = f"SELECT * FROM tbSae WHERE CustCode = '{result}'"
                            order_text = execute_data(query)

                        if not order_text:
                            raise ValueError("No data found in Customer")

                    except Exception as e:
                        print(f"Error Customer: {e}")
                        order_text = []  
 
        if 'button_add' in request.form:
            
            select_value = request.form.get('customer')
            select_stock = request.form.get('stock')

            print("เพิ่ม", select_stock)

            if select_value  is None or select_value == "":
                print("Select value is None")
                return redirect(url_for("home"))
            elif select_stock is None or select_stock == "":
                print("Select stock is None")
                return redirect(url_for("home"))
            elif select_value and select_stock is not None:

                print("Select value:", select_value)
                print("Select stock:", select_stock)

                for row in stock_text:
                    if select_stock == row[0]:
                        stockgrp_code = row[1]

                        query = f"INSERT INTO tbSae (CustCode, StockCode, StockGrpCode,Status) VALUES ('{custcode}', '{select_stock}', '{stockgrp_code}','1')"
                        print("insert: ",execute_data_insert(query))


                customer_result = execute_data(f"SELECT * FROM tbCustomer WHERE Custcode = '{select_value}'")
                if customer_result:
                    cus_name = customer_result[0][3]
                    cus_prefix = customer_result[0][2]
                    cus_tel = customer_result[0][5]

                stock_result = execute_data(f"SELECT * FROM tbStock WHERE Stockcode = '{select_stock}'")
                if stock_result:
                    pro_name = stock_result[0][4]

                
                message_text = (
                    f"📢ร้านคงเดชอวียวะ"
                    f"\n\n📜การสั่งซื้อใหม่📜\n\n 👦🏻ลูกค้า: {cus_prefix} {cus_name} \n 📞เบอร์: {cus_tel} \n 📦nสินค้า: {pro_name}"
                )
                message = {"message": message_text}

                res = requests.post(url=url, headers=headers, data=message)

                select_value = None
                select_stock = None

                return redirect(url_for("home"))
            else:
                print("data to insert is wrong")
                return redirect(url_for("home"))
    
        if 'button_select_edit' in request.form:
            button_select_edit = request.form.get("button_select_edit")  # รับค่าจากฟอร์ม
            print("แก้ไข", button_select_edit)

            if order_text:  # เช็คว่ามีข้อมูลใน order_text ไหม
                for row in order_text:
                    if str(row[0]) == str(button_select_edit):  # แปลงเป็น string ก่อนเช็ค
                        print("พบข้อมูลที่ต้องการแก้ไข:", row[0])

                        select_value = row[1]
                        select_stock = row[2]

                        for row in customer_text:
                            if select_value == row[0]:
                                customergrp_text = row[1]

                        query = "SELECT CustGrpName FROM tbCustomerGrp where CustGrpCode = '" + customergrp_text + "'"
                        result_customergrp = execute_data(query)
                        
                        for result_text in result_customergrp:
                            customergrp_text = result_text[0]

                        print("Select stock:", select_stock)
                        print("Select value:", select_value)
                        

                        select = button_select_edit
                    
                        print("Select", select)
            else:
                print("ไม่มีข้อมูลให้แก้ไข")

        
        if 'button_edit' in request.form:
            button_edit = request.form.get("button_edit")
            old_data = execute_data(f"SELECT CustCode, StockCode FROM tbSae WHERE SOCode='{button_edit}'")

            if old_data:
                custcode_old, stockcode_old = old_data[0]
                customer_result = execute_data(f"SELECT * FROM tbCustomer WHERE Custcode = '{custcode_old}'")
                if customer_result:
                    cus_name_old = customer_result[0][3]
                    cus_prefix_old = customer_result[0][2]
                    cus_tel_old = customer_result[0][5]

            stock_result = execute_data(f"SELECT * FROM tbStock WHERE Stockcode = '{stockcode_old}'")
            if stock_result:
                    pro_name_old = stock_result[0][4]

            print("แก้ไข", button_edit)

            select_value = request.form.get('customer')
            select_stock = request.form.get('stock')

            print("Select value Edit:", custcode)
            print("Select stock: Edit", select_stock)

            custcode = select_value

            if select_value and select_stock is not None:
                for row in stock_text:
                    
                    if select_stock == row[0]:
                        result = row[1]
                        stockgrp_code = result
                        if custcode  is None:
                            print("Select value is None")
                            return redirect(url_for("home"))
                        elif select_stock is None:
                            print("Select stock is None")
                            return redirect(url_for("home"))
                        elif stockgrp_code is None:
                            print("StockGrp is none")
                            return redirect(url_for("home"))
                        elif button_edit is None:
                            print("NO point to update")
                            return redirect(url_for("home"))
                        else:
                            print("Update: ", button_edit)
                            query = f"UPDATE tbSae SET CustCode = '{custcode}', StockCode = '{select_stock}', StockGrpCode = '{stockgrp_code}' WHERE SOCode = '{button_edit}'"
                            print("update: ",execute_data_insert(query))

                            customer_result = execute_data(f"SELECT * FROM tbCustomer WHERE Custcode = '{select_value}'")
                            if customer_result:
                                cus_name = customer_result[0][3]
                                cus_prefix = customer_result[0][2]
                                cus_tel = customer_result[0][5]

                            stock_result = execute_data(f"SELECT * FROM tbStock WHERE Stockcode = '{select_stock}'")
                            if stock_result:
                                pro_name = stock_result[0][4]
                            
                            message_text = (
                                f"📢ร้านคงเดชอวียวะ"
                                f"\n\nมีการแก้ไขการสั่งซื้อ\n\n📤------ข้อมูลเดิม------📤 \n 👦🏻ลูกค้า: {cus_prefix_old} {cus_name_old} \n 📞เบอร์: {cus_tel_old} \n 📦สินค้า: {pro_name_old}"
                                f"\n📥------ข้อมูลใหม่------📥\n 👦🏻ลูกค้า: {cus_prefix} {cus_name} \n 📞เบอร์: {cus_tel} \n 📦สินค้า: {pro_name}"
                            )
                            message = {"message": message_text}

                            res = requests.post(url=url, headers=headers, data=message)

                            select_value = None
                            select_stock = None
                            custcode = None
                            button_select_edit = None

                            return redirect(url_for("home"))
            else:
                        print("data to update is wrong")
                        return redirect(url_for("home"))
        
        if 'button_cancle' in request.form:
            button_cancle = request.form.get("button_cancle")
            print("ยกเลิก", button_cancle)

            select_value = request.form.get('customer')
            select_stock = request.form.get('stock')

            customer_result = execute_data(f"SELECT * FROM tbCustomer WHERE Custcode = '{select_value}'")
            if customer_result:
                cus_name = customer_result[0][3]
                cus_prefix = customer_result[0][2]
                cus_tel = customer_result[0][5]

            stock_result = execute_data(f"SELECT * FROM tbStock WHERE Stockcode = '{select_stock}'")
            if stock_result:
                pro_name = stock_result[0][4]
                            
            message_text = (
                                f"📢ร้านคงเดชอวียวะ"
                                f"\n------รายการสั่งซื้อถูกยกเลิก------ \n 👦🏻ลูกค้า: {cus_prefix} {cus_name} \n 📞เบอร์: {cus_tel} \n 📦สินค้า: {pro_name}"
                            )
            message = {"message": message_text}

            try:
                print("Delete:", button_cancle)
                query = f"UPDATE tbSae SET Status='0' WHERE SOCode=" + button_cancle
                print("Delete Suc", execute_data_insert(query))
                res = requests.post(url=url, headers=headers, data=message)
                return redirect(url_for("home"))
            except Exception as e:
                print(e)
                return redirect(url_for("home"))
            
    else:
        print("Connect database failed")
        return redirect(url_for("home"))

    return render_template("home/home.html",
                            search_tb_text=search_tb_text,
                            button_select_edit=button_select_edit,
                            select_value=select_value,
                            select_stock=select_stock,
                            customer_text=customer_text,
                            stock_text=stock_text,
                            stock_textgrp=stock_textgrp,
                            customergrp_text=customergrp_text,
                            order_text=order_text
                            )


@app.route("/customer")
def customer():
    result = connection_database()

    if result > 0:
        query = "SELECT * FROM tbCustomer"
        result_customer = execute_data(query)
        if result_customer:
            customer_text = result_customer
            print(customer_text)
        else:
            print("fa")
        conn_text = "สำเร็จ"
    else:
        conn_text = "ไม่สำเร็จ"
    return render_template("customer/customer.html",customer_text=customer_text)

@app.route("/customergrp")
def customergrp():
    result = connection_database()

    if result > 0:
        query = "SELECT * FROM tbCustomerGrp"
        result_customer = execute_data(query)

        if result_customer:
            customer_text = result_customer
            print(customer_text)

        else:
            print("fa")
        conn_text = "สำเร็จ"
    else:
        conn_text = "ไม่สำเร็จ"
    return render_template("customergrp/customergrp.html",customer_text=customer_text)

@app.route("/stock")
def stock():
    result = connection_database()

    if result > 0:
        query = "SELECT * FROM tbStock"
        result_stock = execute_data(query)
        if result_stock:
            stock_text = result_stock
        else:
            print("fa")
        conn_text = "สำเร็จ"
    else:
        conn_text = "ไม่สำเร็จ"
    return render_template("stock/stock.html",stock_text=stock_text)

@app.route("/stockgrp")
def stockgrp():
    result = connection_database()

    if result > 0:
        query = "SELECT * FROM tbStockGrp"
        result_stock = execute_data(query)
        if result_stock:
            stock_text = result_stock
        else:
            print("fa")
        conn_text = "สำเร็จ"
    else:
        conn_text = "ไม่สำเร็จ"
    return render_template("stockgrp/stockgrp.html",stock_text=stock_text)

@app.route("/saletype")
def saletype():
    result = connection_database()

    if result > 0:
        query = "SELECT * FROM tbSaleType"
        result_saletype = execute_data(query)
        if result_saletype:
            saletype_text = result_saletype
        else:
            print("fa")
        conn_text = "สำเร็จ"
    else:
        conn_text = "ไม่สำเร็จ"
    return render_template("saletype/saletype.html",saletype_text=saletype_text)

@app.route("/location")
def location():
    result = connection_database()

    if result > 0:
        query = "SELECT * FROM tbLocation"
        result_location = execute_data(query)
        if result_location:
            location_text = result_location
        else:
            print("fa")
        conn_text = "สำเร็จ"
    else:
        conn_text = "ไม่สำเร็จ"
    return render_template("location/location.html",location_text=location_text)





if __name__ == "__main__":
    app.run(debug=True)