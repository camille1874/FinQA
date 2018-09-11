from flask import Flask,request,render_template,redirect

app = Flask(__name__)
#绑定访问地址127.0.0.1:5000/user
@app.route("/qa",methods=['GET','POST'])
def login():
    if request.method =='POST':
        question = request.form['question']
        value = request.form['chose']
        if value == '1':
            return redirect('http://www.bilibili.com')
        if question =="user":
            return redirect("http://www.baidu.com")
        else:
            message = "未找到答案"
            return render_template('login.html',message=message)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
