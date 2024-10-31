from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
from django import forms
from .forms import Supplier_Form
from .forms import Category_Form
import sqlite3

def login_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    data = {}
    var = []
    try:
        if request.method == 'POST':
            uname = request.POST.get('username')
            upassword = request.POST.get('pass')
            cur.execute('SELECT Empno FROM Employee WHERE ENAME = ?;', (uname,))
            row = cur.fetchall()
            if row:
                cur.execute('SELECT UserType, Password FROM Login WHERE Empno = ?;', (row[0][0],))
                check = cur.fetchall()
                if check:
                    c = [('Admin', upassword), ('Retailer', upassword)]
                    for i in range(len(check)):
                        if check[i] in c:
                            var += check[i]
                    if var[0] == 'Admin' and var[1] == upassword:
                        return HttpResponseRedirect('/main_menu/')
                    elif var[0] == 'Retailer' and var[1] == upassword:
                        return HttpResponseRedirect('/customer/')
            else:
                return HttpResponseRedirect('/')
            conn.close()
    except:
        pass
    else:
        conn.close()
        pass
    conn.close()
    
    return render(request, 'logins.html', data)

def logout_page(request):
    return HttpResponseRedirect('/')

def main_menu_page(request):
    curr_time = datetime.now().time()
    curr_date = datetime.now().date()
    data = {'curr_time':curr_time, 'curr_date':curr_date}
    return render(request, 'main_menu.html', data)

def supplier_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == 'POST':
        fm = Supplier_Form(request.POST)
        nm = request.POST.get('Name')
        cont = request.POST.get('Contact')
        desc = request.POST.get('Description')
        cur.execute("INSERT INTO Supplier (SUP_NAME, SUP_CONTACT, SUP_DESCRIPTION) VALUES(?, ?, ?)", (nm, cont, desc))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/supplier_page/')
    else:
        fm = Supplier_Form()
    cur.execute('SELECT * FROM Supplier_View;')
    rows = cur.fetchall()
    data = {'form':fm, 'sup':rows}
    conn.close()
    return render(request, 'suppliers.html', data)

def update_sup(request, id):
    class Supplier_update_Form(forms.Form):
            Name = forms.CharField(label='Sup Name', widget=forms.TextInput(attrs={'class':'form-control'}))
            Contact = forms.CharField(label='Sup Contact', widget=forms.TextInput(attrs={'class':'form-control'}))
            Description = forms.CharField(label='Sup Description', widget=forms.Textarea(attrs={'class':'form-control'}))
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        nm = request.POST.get('Name')
        cont = request.POST.get('Contact')
        desc = request.POST.get('Description')
        cur.execute("UPDATE Supplier SET SUP_NAME = ?, SUP_CONTACT = ?, SUP_DESCRIPTION = ? WHERE SUPID = ?;", (nm, cont, desc, id))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/supplier_page/')
    else:
        cur.execute("SELECT * FROM SUPPLIER WHERE SUPID = ?", (id,))
        f = cur.fetchall()
        initial_data = {
            "Name":f[0][1],
            "Contact":f[0][2],
            "Description":f[0][3]
        }
        fm = Supplier_update_Form(initial=initial_data)
    conn.close()
    return render(request, 'update_supplier.html', {'form_upd':fm})

def delete_sup(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("DELETE FROM Supplier WHERE SUPID = ?;", (id,))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/supplier_page/')
    conn.close()
    
def category_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == 'POST':
        fm = Category_Form(request.POST)
        c_nm = request.POST.get('Category_Name')
        cur.execute("INSERT INTO Category (CAT_NAME) VALUES (?);", (c_nm,))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/category/')
    else:
        fm = Category_Form()
    cur.execute('SELECT * FROM Category_View;')
    rows = cur.fetchall()
    data = {'form_cat':fm, 'cat':rows}
    conn.close()
    return render(request, 'categories.html', data)

def delete_cat(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("DELETE FROM Category WHERE CID = ?;", (id,))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/category/')
    conn.close()
    
def product_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    class Product_Form(forms.Form):
        cur.execute("SELECT Sup_Name FROM Supplier;")
        x=cur.fetchall()
        lst = [('Select','Select')]
        for i in x:
            c = []
            for j in i[0:1]:
                c.append(j)
                c.append(j)
            lst.append(tuple(c))
        cur.execute("SELECT CAT_NAME FROM Category;")
        y=cur.fetchall()
        lst1 = [('Select','Select')]
        for k in y:
            a = []
            for m in k[0:1]:
                a.append(m)
                a.append(m)
            lst1.append(tuple(a))
        Product_Name = forms.CharField(label='Product Name', widget=forms.TextInput(attrs={'class':'form-control'}))
        Price = forms.CharField(label='Price', widget=forms.TextInput(attrs={'class':'form-control'}))
        Quantity = forms.CharField(label='Quantity', widget=forms.TextInput(attrs={'class':'form-control'}))
        Category = forms.ChoiceField(choices=lst1)
        Supplier = forms.ChoiceField(choices=lst)
        Status = forms.ChoiceField(choices=[('Select','Select'),('Active', 'Active'), ('Inactive', 'Inactive')])
    try:
        if request.method == 'POST':
            fm = Product_Form(request.POST)
            pro_nm = request.POST.get('Product_Name')
            pro_price = request.POST.get('Price')
            pro_qty = request.POST.get('Quantity')
            pro_stat = request.POST.get('Status')
            pro_cat = request.POST.get('Category')
            pro_sup = request.POST.get('Supplier')
            cur.execute('SELECT CID FROM Category WHERE CAT_NAME = ?;', (pro_cat,))
            s = cur.fetchall()
            q = s[0][0]
            cur.execute('SELECT SUPID FROM Supplier WHERE Sup_Name = ?;', (pro_sup,))
            w = cur.fetchall()
            u = w[0][0]
            cur.execute("INSERT INTO Product(Pro_Name, Pro_Price, Pro_QTY, Pro_Status, CID, SUPID) VALUES(?,?,?,?,?,?);", (pro_nm, int(pro_price), int(pro_qty), pro_stat, q, u))
            conn.commit()
            conn.close()
            return HttpResponseRedirect('/product/')
        else:
            fm = Product_Form()
    except:
        pass
    cur.execute('SELECT Product.PID, Product.Pro_Name, Product.Pro_Price, Product.Pro_QTY, Product.Pro_Status, Category.CAT_NAME, Supplier.Sup_Name FROM Product LEFT JOIN Category ON Product.CID = Category.CID LEFT JOIN Supplier ON Product.SUPID = Supplier.SUPID;')
    rows = cur.fetchall()
    data = {'form':fm, 'pro':rows}
    conn.close()
    return render(request, 'products.html', data)

def delete_pro(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("DELETE FROM Product WHERE PID = ?;", (id,))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/product/')
    conn.close()
    
def update_pro(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    class Product_upd_Form(forms.Form):
        cur.execute("SELECT Sup_Name FROM Supplier;")
        x=cur.fetchall()
        lst = [('Select','Select')]
        for i in x:
            c = []
            for j in i[0:1]:
                c.append(j)
                c.append(j)
            lst.append(tuple(c))
        cur.execute("SELECT CAT_NAME FROM Category;")
        y=cur.fetchall()
        lst1 = [('Select','Select')]
        for k in y:
            a = []
            for m in k[0:1]:
                a.append(m)
                a.append(m)
            lst1.append(tuple(a))
        Product_Name = forms.CharField(label='Product Name', widget=forms.TextInput(attrs={'class':'form-control'}))
        Price = forms.CharField(label='Price', widget=forms.TextInput(attrs={'class':'form-control'}))
        Quantity = forms.CharField(label='Quantity', widget=forms.TextInput(attrs={'class':'form-control'}))
        Category = forms.ChoiceField(choices=lst1)
        Supplier = forms.ChoiceField(choices=lst)
        Status = forms.ChoiceField(choices=[('Select','Select'),('Active', 'Active'), ('Inactive', 'Inactive')]) 
    if request.method == "POST":
        pro_nm = request.POST.get('Product_Name')
        pro_price = request.POST.get('Price')
        pro_qty = request.POST.get('Quantity')
        pro_stat = request.POST.get('Status')
        pro_cat = request.POST.get('Category')
        pro_sup = request.POST.get('Supplier')
        cur.execute('SELECT CID FROM Category WHERE CAT_NAME = ?;', (pro_cat,))
        s = cur.fetchall()
        q = s[0][0]
        cur.execute('SELECT SUPID FROM Supplier WHERE Sup_Name = ?;', (pro_sup,))
        w = cur.fetchall()
        u = w[0][0]
        cur.execute("UPDATE Product SET Pro_Name = ?, Pro_Price = ?, Pro_Qty = ?, Pro_Status = ?, CID = ?, SUPID = ? WHERE PID = ?;", (pro_nm, pro_price, pro_qty, pro_stat, q, u, id))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/product/')
    else:
        cur.execute("SELECT Product.PID, Product.Pro_Name, Product.Pro_Price, Product.Pro_QTY, Product.Pro_Status, Category.CAT_NAME, Supplier.Sup_Name FROM Product LEFT JOIN Category ON Product.CID = Category.CID LEFT JOIN Supplier ON Product.SUPID = Supplier.SUPID WHERE PID = ?;", (id,))
        v = cur.fetchall()

        
        initial_data = {
            'Product_Name':v[0][1],
            'Price':v[0][2],
            'Quantity':v[0][3],
            'Status':v[0][4],
            'Category':v[0][5],
            'Supplier':v[0][6],
        }
        fm = Product_upd_Form(initial=initial_data)
    conn.close()
    return render(request, 'update_product.html', {'form_upd':fm})

def employee_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    try:
        if request.method == 'POST':
            emp_nm = request.POST.get('Empname')
            emp_contact = request.POST.get('Empcontact')
            emp_dob = request.POST.get('Empdbo')
            emp_hiredate = request.POST.get('Emphiredate')
            emp_email = request.POST.get('Empemail')
            emp_gender = request.POST.get('Empgender')
            emp_type = request.POST.get('Emptype')
            emp_pass = request.POST.get('Emppass')
            emp_salary = request.POST.get('Empsalary')
            emp_address = request.POST.get('Empaddress')
            cur.execute("SELECT EMPNO FROM EMPLOYEE WHERE ENAME = ? AND EMAIL = ? AND GENDER = ? AND CONTACT = ? AND DOB = ? AND HIREDATE = ? AND ADDRESS = ? AND SALARY = ?;", (emp_nm, emp_email, emp_gender, emp_contact, emp_dob, emp_hiredate, emp_address, int(emp_salary)))
            f = cur.fetchall()
            if f:
                cur.execute("SELECT UserType, Password FROM LOGIN WHERE EMPNO = ?;", (f[0][0],))
                h = cur.fetchall()
                if emp_type != h[0][0] and emp_pass != h[0][1]:
                    cur.execute("INSERT INTO Login(Empno, UserType, Password) VALUES (?, ?, ?)", (f[0][0], emp_type, emp_pass))
                    conn.commit()
                    conn.close()
            else:
                cur.execute("INSERT INTO Employee(ENAME, EMAIL, GENDER, CONTACT, DOB, HIREDATE, ADDRESS, SALARY) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (emp_nm, emp_email, emp_gender, emp_contact, emp_dob, emp_hiredate, emp_address, int(emp_salary)))
                conn.commit()
                cur.execute("SELECT Empno FROM Employee ORDER BY Empno DESC LIMIT 1;")
                id = cur.fetchone()
                cur.execute("INSERT INTO Login(Empno, UserType, Password) VALUES (?, ?, ?)", (id[0], emp_type, emp_pass))
                conn.commit()
                conn.close()
            return HttpResponseRedirect('/employee/')
    except:
        pass
    cur.execute('SELECT * FROM Employee_View;')
    rows = cur.fetchall()
    data = {'emp':rows}
    conn.close()
    return render(request, 'employees.html', data)

def delete_emp(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("DELETE FROM Employee WHERE Empno = ?;", (id,))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/employee/')
    conn.close()
    
def update_emp(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    data = {}
    try:
        if request.method == "POST":
            emp_nm = request.POST.get('Empname')
            emp_contact = request.POST.get('Empcontact')
            emp_address = request.POST.get('Empaddress')
            emp_salary = request.POST.get('Empsalary')
            emp_dob = request.POST.get('Empdbo')
            emp_hiredate = request.POST.get('Emphiredate')
            emp_email = request.POST.get('Empemail')
            emp_type = request.POST.get('Emptype')
            emp_pass = request.POST.get('Emppass')
            emp_gender = request.POST.get('Empgender')
            cur.execute("UPDATE EMPLOYEE SET ENAME = ?, EMAIL = ?, GENDER = ?, CONTACT = ?, DOB = ?, HIREDATE = ?, ADDRESS = ?, SALARY = ? WHERE Empno = ?;", (emp_nm, emp_email, emp_gender, emp_contact, emp_dob, emp_hiredate, emp_address, int(emp_salary), id))
            conn.commit()
            cur.execute("UPDATE Login SET UserType = ?, Password = ? WHERE Empno = ?;", (emp_type, emp_pass, id))
            conn.commit()
            conn.close()
            return HttpResponseRedirect('/employee/')
    except:
        pass
    else:
        cur.execute('SELECT * FROM Employee_View WHERE Empno = ?;', (id,))
        rows = cur.fetchall()
        cur.execute("SELECT USERTYPE, PASSWORD FROM LOGIN WHERE Empno = ?", (id,))
        l = cur.fetchall()
        print(l)
        data = {
            'name':rows[0][1],
            'email':rows[0][2],
            'gender':rows[0][3],
            'contact':rows[0][4],
            'dob':rows[0][5],
            'hire':rows[0][6],
            'address':rows[0][7],
            'salary':rows[0][8],
            'user':l[0][0],
            'pass_emp':l[0][1]
        }
    conn.close()
    return render(request, 'update_employee.html', data)

def billing_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        search = request.POST.get('search')
        cur.execute("SELECT PID, Pro_Name, Pro_Price, Pro_Qty, Pro_Status FROM Product WHERE Pro_Status = 'Active' AND Pro_Qty > 0 AND Pro_Name = ?;", (search,))
        rows = cur.fetchall()
    else:
        cur.execute("SELECT PID, Pro_Name, Pro_Price, Pro_Qty, Pro_Status FROM Product WHERE Pro_Status = 'Active' AND Pro_Qty > 0;")
        rows = cur.fetchall()
    data = {'pro':rows}
    conn.close()
    return render(request, 'billing.html', data)

def customer_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    try:
        if request.method == "POST":
            cus_nm = request.POST.get('cus_name')
            cus_contact = request.POST.get('cus_contact')
            curr_date = datetime.now().date()
            cur.execute("SELECT CUS_ID FROM Customer WHERE Name = ? AND Contact = ?;", (cus_nm, cus_contact))
            a = cur.fetchall()
            if a:
                cur.execute("INSERT INTO BILL (CUS_ID, BILL_DATE) VALUES (?, ?);", [a[0][0], curr_date])
                conn.commit()
                conn.close()
                return HttpResponseRedirect('/billing_page/')
            else:
                cur.execute("INSERT INTO Customer (Name, Contact) VALUES (?, ?);", (cus_nm, cus_contact))
                conn.commit()
                cur.execute("SELECT CUS_ID FROM Customer ORDER BY CUS_ID DESC LIMIT 1;")
                id = cur.fetchone()
                cur.execute("INSERT INTO BILL (CUS_ID, BILL_DATE) VALUES (?, ?);", [id[0], curr_date])
                conn.commit()
                conn.close()
                return HttpResponseRedirect('/billing_page/')
    except:
        pass
    return render(request, 'customer.html')

def process_cart(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        qty = request.POST.get('cus_qty')
        cur.execute("SELECT BILL_NO FROM Bill ORDER BY BILL_NO DESC LIMIT 1;")
        z = cur.fetchall()
        cur.execute("SELECT PID FROM Bill_Detail WHERE PID = ? AND BILL_NO = (SELECT BILL_NO FROM Bill ORDER BY BILL_NO DESC LIMIT 1);", (id,))
        w = cur.fetchall()
        if w:
            cur.execute("SELECT Pro_Qty FROM Product WHERE PID = ?;", (id,))
            g = cur.fetchall()
            if g[0][0] >= int(qty):
                cur.execute("UPDATE Bill_Detail SET QTY = (QTY + ?) WHERE PID = ? AND BILL_NO = (SELECT BILL_NO FROM Bill ORDER BY BILL_NO DESC LIMIT 1);" , (qty, id))
                conn.commit()
                cur.execute("UPDATE Product SET Pro_Qty = (Pro_Qty - ?) WHERE PID = ?;", (qty, id))
                conn.commit()
        else:
            cur.execute("SELECT Pro_Qty FROM Product WHERE PID = ?;", (id,))
            g = cur.fetchall()
            if g[0][0] >= int(qty):
                cur.execute('INSERT INTO Bill_Detail (BILL_NO, PID, QTY) VALUES (?,?,?);', (z[0][0], id, qty))
                conn.commit()
                cur.execute("UPDATE Product SET Pro_Qty = (Pro_Qty - ?) WHERE PID = ?;", (qty, id))
                conn.commit()
            else:
                return HttpResponseRedirect('/billing_page/')
        conn.close()
        return HttpResponseRedirect('/billing_page/')
    else:
        conn.close()
        return HttpResponseRedirect('/billing_page/')
    
def cart_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "GET":
        cur.execute("SELECT Bill_Detail.PID, Product.Pro_Name, Bill_Detail.QTY, Product.Pro_Price FROM Product INNER JOIN Bill_Detail ON Product.PID = Bill_Detail.PID WHERE BILL_NO = (SELECT BILL_NO FROM Bill ORDER BY BILL_NO DESC LIMIT 1);")
        row = cur.fetchall()
        result = []
        for i in row:
            j = list(i)
            p = j.pop(3)
            q = j.pop(2)
            r = p*q
            j.append(p)
            j.append(q)
            j.append(r)
            result.append(tuple(j))
        cur.execute("SELECT Product.Pro_Price, Bill_Detail.QTY FROM Product INNER JOIN Bill_Detail ON Product.PID = Bill_Detail.PID  WHERE BILL_NO = (SELECT BILL_NO FROM Bill ORDER BY BILL_NO DESC LIMIT 1);")
        a = cur.fetchall()
        sum = 0
        for i in a:
            k = i[0] * i[1]
            sum += k
        conn.close()
    conn.close()
    data = {'cart':result, 'sum':sum}
    return render(request, 'cart.html', data)

def delete_cart(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("SELECT QTY FROM Bill_Detail WHERE PID = ? AND BILL_NO = (SELECT BILL_NO FROM Bill ORDER BY BILL_NO DESC LIMIT 1);", (id,))
        q = cur.fetchall()
        cur.execute("UPDATE Product SET Pro_QTY = (Pro_Qty + ?) WHERE PID = ?;", (q[0][0], id))
        conn.commit()
        cur.execute('DELETE FROM Bill_Detail WHERE PID = ? AND BILL_NO = (SELECT BILL_NO FROM Bill ORDER BY BILL_NO DESC LIMIT 1);', (id,))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/cart/')
    
def bill(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    data = {}
    if request.method == "GET":
        cur.execute("SELECT BILL_NO, BILL_DATE FROM Bill ORDER BY BILL_NO DESC LIMIT 1;")
        j = cur.fetchall()
        data['billd'] = j
        cur.execute("SELECT NAME, CONTACT FROM CUSTOMER ORDER BY CUS_ID DESC LIMIT 1;")
        rows = cur.fetchall()
        data['cust'] = rows
        cur.execute("SELECT Category.CAT_NAME, Bill_Detail.QTY, Product.PRO_NAME, Product.PRO_PRICE FROM PRODUCT INNER JOIN BILL_DETAIL ON PRODUCT.PID = BILL_DETAIL.PID INNER JOIN CATEGORY ON PRODUCT.CID = CATEGORY.CID  WHERE BILL_NO = (SELECT BILL_NO FROM Bill ORDER BY BILL_NO DESC LIMIT 1);")
        m = cur.fetchall()
        r = []
        sum = 0
        for i in m:
            e = [i[0], i[1], i[2], i[3]]
            f = i[1]
            g = i[3]
            h = f*g
            sum += h
            e.append(h)
            r.append(tuple(e))
        data['selected_p'] = r
        data['total'] = sum
        #cur.execute("DELETE FROM BILL_DETAIL;")
        #conn.commit()
        conn.close()
    conn.close()
    return render(request, 'bill.html', data)


def sales_page(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    
    if request.method == "GET":
        cur.execute("SELECT BILL.BILL_NO, BILL.BILL_DATE, BILL.CUS_ID, CUSTOMER.NAME, BILL.BILL_DATE FROM BILL INNER JOIN CUSTOMER ON BILL.CUS_ID = CUSTOMER.CUS_ID;")
        rows = cur.fetchall()
        conn.close()
    else:
        search_method = request.POST.get('search_method')
        search = request.POST.get('search')
        print(search, search_method)
        if search_method == "Bill No.":
            cur.execute("SELECT BILL.BILL_NO, BILL.BILL_DATE, BILL.CUS_ID, CUSTOMER.NAME, BILL.BILL_DATE FROM BILL INNER JOIN CUSTOMER ON BILL.CUS_ID = CUSTOMER.CUS_ID WHERE BILL_NO = ?;", (search,))
            rows = cur.fetchall()
            conn.close()
        elif search_method == "Customer Name":
            cur.execute("SELECT BILL.BILL_NO, BILL.BILL_DATE, BILL.CUS_ID, CUSTOMER.NAME, BILL.BILL_DATE FROM BILL INNER JOIN CUSTOMER ON BILL.CUS_ID = CUSTOMER.CUS_ID WHERE NAME = ?;", (search,))
            rows = cur.fetchall()
            conn.close()
    data = {'report':rows}
    return render(request, 'sales.html', data)

def getsales(request, id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    data = {}
    if request.method == "POST":
        cur.execute("SELECT BILL_DATE FROM Bill WHERE BILL_NO = ?;", (id,))
        j = cur.fetchall()
        data['billd'] = j
        cur.execute("SELECT CUSTOMER.NAME, CUSTOMER.CONTACT FROM CUSTOMER INNER JOIN BILL ON CUSTOMER.CUS_ID = BILL.CUS_ID WHERE BILL_NO = ?;", (id,))
        rows = cur.fetchall()
        data['cust'] = rows
        cur.execute("SELECT Category.CAT_NAME, Bill_Detail.QTY, Product.PRO_NAME, Product.PRO_PRICE FROM PRODUCT INNER JOIN BILL_DETAIL ON PRODUCT.PID = BILL_DETAIL.PID INNER JOIN CATEGORY ON PRODUCT.CID = CATEGORY.CID  WHERE BILL_NO = ?;", (id,))
        m = cur.fetchall()
        r = []
        sum = 0
        for i in m:
            e = [i[0], i[1], i[2], i[3]]
            f = i[1]
            g = i[3]
            h = f*g
            sum += h
            e.append(h)
            r.append(tuple(e))
        data['selected_p'] = r
        data['total'] = sum
        #cur.execute("DELETE FROM BILL_DETAIL;")
        #conn.commit()
        conn.close()
    conn.close()
    return render(request, 'report.html', data)