from flask import render_template
from App import app,db
from App.models import Block

#删除/创建数据库
# db.drop_all()
# db.create_all()

@app.route('/')
def index():
    blocks=Block.getBlocks()
    return render_template('index.html',blocks=blocks)

if __name__ == '__main__':
    app.run(port=8080,debug=True)