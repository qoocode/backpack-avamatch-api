from flask import Flask,Request
from flask_restful import Resource,Api,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy,Model

app = Flask(__name__)

#----- database -----
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
api=Api(app)


class UserModel(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    customer_id=db.Column(db.Integer,nullable=False)
    element_id=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"User(user_id={user_id},user_name={user_name},password={password},customer_id={customer_id},elment_id={element_id})"

class PreElementModel(db.Model):
    element_id=db.Column(db.Integer,primary_key=True)
    element_name=db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return f"PreElement(element_id={element_id},element_name={element_name})"

class PreElementDateModel(db.Model):
    date_id=db.Column(db.Integer,primary_key=True)
    start_date=db.Column(db.String(10),nullable=False)
    end_date=db.Column(db.String(10),nullable=False)
    element_id=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"PreElemnentDate(date_id={date_id},start_date={start_date},end_date={end_date},element_id={element_id})" 

class CustomerModel(db.Model):
    customer_id=db.Column(db.Integer,primary_key=True)
    customer_name=db.Column(db.String(45),nullable=False)
    birth_day=db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Customer(customer_id={customer_id},customer_name={customer_name},birth_day={birth_day})"

class AvatarModel(db.Model):
    avatar_id=db.Column(db.Integer,primary_key=True)
    avatar_name=db.Column(db.String(40),nullable=False) 
    avatar_image=db.Column(db.String(50),nullable=True)

    def __repr__(self):
        return f"Avatar(avatar_id={avatar_id},avatar_name={avatar_name},avatar_image={avatar_image})"

class UserAvatarModel(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    avatar_id=db.Column(db.Integer,nullable=False)
    avatar_nickname=db.Column(db.String(50),nullable=False)
    level=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return f"user_id={user_id},avatar_id={avatar_id},avatar_nickname={avatar_nickname},level={level}"

class ProductModel(db.Model):
    product_code=db.Column(db.String(10),primary_key=True)
    product_name=db.Column(db.String(50),nullable=False)
    risk_level=db.Column(db.Integer,nullable=False)
    
    def __repr__(self):
        return f"product_code={product_code},product_name={product_name},risk_level={risk_level}"

class ProductGroupModel(db.Model):
    element_id=db.Column(db.Integer,primary_key=True)
    product_code=db.Column(db.String(10),primary_key=True)

    def __repr__(self):
        return f"element_id={element_id},product_code={ product_code}"

class UserPortfolioModel(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    seq_no=db.Column(db.Integer,primary_key=True)
    product_code=db.Column(db.String(10),nullable=False)
    initial_unit=db.Column(db.Float,nullable=False)
    initial_amount=db.Column(db.Float,nullable=False)
    current_amount=db.Column(db.Float,nullable=False)
    create_date=db.Column(db.String(10),nullable=False)

    def __repr__(self):
        return f"user_id={user_id},seq_no={seq_no},intiial_unit={intiial_unit},product_code={product_code},intiial_unit={intiial_unit},initial_amount={initial_amount},current_amount={current_amount},create_date={create_date}"

class QuestionairModel(db.Model):
    question_id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.String(100),primary_key=True)

    def __repr__(self):
        return f"question_id={question_id},question={question}"

db.create_all()

user_add_args=reqparse.RequestParser()
user_add_args.add_argument("user_name",type=str,required=True,help="user_name is empty.")
user_add_args.add_argument("password",type=str,required=False)
user_add_args.add_argument("customer_id",type=int,required=False)
user_add_args.add_argument("element_id",type=int,required=False)

user_field={
    "user_id":fields.Integer,
    "user_name":fields.String,
    "password":fields.String,
    "customer_id":fields.Integer,
    "element_id":fields.Integer
}

customer_add_args=reqparse.RequestParser()
customer_add_args.add_argument("customer_name",type=str,required=False)
customer_add_args.add_argument("birth_day",type=str,required=False)

customer_field={
    "customer_id":fields.Integer,
    "customer_name":fields.String,
    "birth_day":fields.String
}

user_avatar_add_args=reqparse.RequestParser()
user_avatar_add_args.add_argument("avatar_id",type=int,required=False)
user_avatar_add_args.add_argument("avatar_nickname",type=str,required=False)
user_avatar_add_args.add_argument("level",type=int,required=False)

user_avatar_field={
    "user_id":fields.Integer,
    "avatar_id":fields.Integer,
    "avatar_nickname":fields.String,
    "level":fields.Integer
}

user_portfolio_add_args=reqparse.RequestParser()
user_portfolio_add_args.add_argument("seq_no",type=int,required=True,help="seq_no is empty.")
user_portfolio_add_args.add_argument("product_code",type=str,required=False)
user_portfolio_add_args.add_argument("initial_unit",type=float,required=False)
user_portfolio_add_args.add_argument("initial_amount",type=float,required=False)
user_portfolio_add_args.add_argument("current_amount",type=float,required=False)
user_portfolio_add_args.add_argument("create_date",type=str,required=False)

user_portfolio_field={
    "user_id":fields.Integer,
    "seq_no":fields.Integer,
    "product_code":fields.String,
    "initial_unit":fields.Float,
    "initial_amount":fields.Float,
    "current_amount":fields.Float,
    "create_date":fields.String
}

questionair_add_args=reqparse.RequestParser()
questionair_add_args.add_argument("question",type=str,required=True,help="question is empty.")

question_field={
    "question_id":fields.Integer,
    "question":fields.String
}

pre_element_add_args=reqparse.RequestParser()
pre_element_add_args.add_argument("element_name",type=str,required=True,help="element_name is empty.")

pre_element_field={
    "element_id":fields.Integer,
    "element_name":fields.String
}

pre_element_date_add_args=reqparse.RequestParser()
pre_element_date_add_args.add_argument("date_id",type=int,required=True,help="date_is is empty.")
pre_element_date_add_args.add_argument("start_date",type=str,required=False)
pre_element_date_add_args.add_argument("end_date",type=str,required=False)
pre_element_date_add_args.add_argument("element_id",type=str,required=False)

pre_element_date_field={
    "date_id":fields.Integer,
    "start_date":fields.String,
    "end_date":fields.String,
    "element_id":fields.Integer
}

product_add_args=reqparse.RequestParser()
product_add_args.add_argument("product_code",type=str,required=True,help="product_code is empty.")
product_add_args.add_argument("product_name",type=str,required=False)
product_add_args.add_argument("risk_level",type=int,required=False)

product_field={
    "product_code":fields.String,
    "product_name":fields.String,
    "risk_level":fields.Integer
}

product_group_add_args=reqparse.RequestParser()
product_group_add_args.add_argument("element_id",type=int,required=True,help="element_id is empty.")
product_group_add_args.add_argument("product_code",type=str,required=False)

product_group_field={
    "element_id":fields.Integer,
    "product_code":fields.String
}

avatar_add_args=reqparse.RequestParser()
avatar_add_args.add_argument("avatar_name",type=str,required=False)
avatar_add_args.add_argument("avatar_image",type=str,required=False)

avatar_field={
    "avatar_name":fields.String,
    "avatar_image":fields.String
}

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello hack day!</h1><p>BACK PACK TEAM</p>"

class User(Resource):

    @marshal_with(user_field)
    def get(self,user_id):
        result=UserModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404,message="Data not found.")
        return result
    
    @marshal_with(user_field)
    def post(self,user_id):
        result=UserModel.query.filter_by(user_id=user_id).first()
        if result:
            abort(409,message="Duplicate data.")
        args=user_add_args.parse_args()
        user=UserModel(user_id=user_id,user_name=args["user_name"],password=args["password"],customer_id=args["customer_id"],element_id=args["element_id"])
        db.session.add(user)
        db.session.commit()
        return user,201

    @marshal_with(user_field)
    def patch(self,user_id):
        args=user_add_args.parse_args()
        result=UserModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404,message="Data not found.")
        if args["password"]:
            result.password=args["password"]
        if args["element_id"]:
            result.element_id=args["element_id"]
        db.session.commit()
        return result
    
    def delete(self,user_id):
        result=UserModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class Customer(Resource):
    @marshal_with(customer_field)   
    def get(self,customer_id):
        result=CustomerModel.query.filter_by(customer_id=customer_id).first()
        if not result:
            abort(404,message="Data not found.")
        return result
    
    @marshal_with(customer_field)
    def post(self,customer_id):
        result=CustomerModel.query.filter_by(customer_id=customer_id).first()
        if result:
            abort(409,message="Duplicate data.")
        args=customer_add_args.parse_args()
        customer=CustomerModel(customer_id=customer_id,customer_name=args["customer_name"],birth_day=args["birth_day"])
        db.session.add(customer)
        db.session.commit()
        return customer,201

    @marshal_with(customer_field)
    def patch(self,customer_id):
        args=customer_add_args.parse_args()
        result=CustomerModel.query.filter_by(customer_id=customer_id).first()
        if not result:
            abort(404,message="Data not found.")
        if args["customer_name"]:
            result.customer_name=args["customer_name"]
        if args["birth_day"]:
            result.birth_day=args["birth_day"]
        db.session.commit()
        return result
    
    def delete(self,customer_id):
        result=CustomerModel.query.filter_by(customer_id=customer_id).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class UserAvatar(Resource):
    @marshal_with(user_avatar_field)   
    def get(self,user_id):
        result=UserAvatarModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404,message="Data not found.")
        return result
   
    @marshal_with(user_avatar_field)
    def post(self,user_id):
        result=UserAvatarModel.query.filter_by(user_id=user_id).first()
        if result:
            abort(409,message="Duplicate data.")
        args=user_avatar_add_args.parse_args()
        user=UserAvatarModel(user_id=user_id,avatar_id=args["avatar_id"],avatar_nickname=args["avatar_nickname"],level=args["level"])
        db.session.add(user)
        db.session.commit()
        return user,201

    @marshal_with(user_avatar_field)
    def patch(self,user_id):
        args=user_avatar_add_args.parse_args()
        result=UserAvatarModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404,message="Data not found.")
        if args["avatar_id"]:
            result.avatar_id=args["avatar_id"]
        if args["avatar_nickname"]:
            result.avatar_nickname=args["avatar_nickname"]
        if args["level"]:
            result.level=args["level"]
        db.session.commit()
        return result
    
    def delete(self,user_id):
        result=UserAvatarModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class UserPortfolio(Resource):
    
    @marshal_with(user_portfolio_field)    
    def get(self,user_id):
        args=user_portfolio_add_args.parse_args()
        if args["seq_no"] == 0:                     
            result=UserPortfolioModel.query.filter_by(user_id=user_id).all()
        else:
            result=UserPortfolioModel.query.filter_by(user_id=user_id,seq_no=args["seq_no"]).all()
        if not result:
            abort(404,message="Data not found.")
        return result
   
    @marshal_with(user_portfolio_field)
    def post(self,user_id):
        args=user_portfolio_add_args.parse_args()
        result=UserPortfolioModel.query.filter_by(user_id=user_id,seq_no=args["seq_no"]).first()
        if result:
            abort(409,message="Duplicate data.")
        user=UserPortfolioModel(user_id=user_id,seq_no=args["seq_no"],product_code=args["product_code"],initial_unit=args["initial_unit"],initial_amount=args["initial_amount"],current_amount=args["current_amount"],create_date=args["create_date"])
        db.session.add(user)
        db.session.commit()
        return user,201

    @marshal_with(user_portfolio_field)
    def patch(self,user_id):
        args=user_portfolio_add_args.parse_args()
        seq_no=args["seq_no"]
        result=UserPortfolioModel.query.filter_by(user_id=user_id,seq_no=args["seq_no"]).first()
        if not result:
            abort(404,message="Data not found.")
        if args["current_amount"]:
            result.current_amount=args["current_amount"]
        db.session.commit()
        return result
    
    @marshal_with(user_portfolio_field)
    def delete(self,user_id):
        args=user_portfolio_add_args.parse_args()
        result=UserPortfolioModel.query.filter_by(user_id=user_id,seq_no=args["seq_no"]).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class Questionair(Resource):
    @marshal_with(question_field)
    def get(self,question_id):
        result=QuestionairModel.query.filter_by(question_id=question_id).first()
        if not result:
            abort(404,message="Data not found.")
        return result
    
    @marshal_with(question_field)
    def post(self,question_id):
        result=QuestionairModel.query.filter_by(question_id=question_id).first()
        if result:
            abort(409,message="Duplicate data.")
        args=questionair_add_args.parse_args()
        question=QuestionairModel(question_id=question_id,question=args["question"])
        db.session.add(question)
        db.session.commit()
        return question,201

    @marshal_with(question_field)
    def patch(self,question_id):
        args=question_add_args.parse_args()
        result=QuestionairModel.query.filter_by(question_id=question_id).first()
        if not result:
            abort(404,message="Data not found.")
        if args["question"]:
            result.password=args["question"]
        db.session.commit()
        return result
    
    def delete(self,question_id):
        result=QuestionairModel.query.filter_by(question_id=question_id).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class PreElement(Resource):
    @marshal_with(pre_element_field)
    def get(self,element_id):
        result=PreElementModel.query.filter_by(element_id=element_id).first()
        if not result:
            abort(404,message="Data not found.")
        return result
    
    @marshal_with(pre_element_field)
    def post(self,element_id):
        result=PreElementModel.query.filter_by(element_id=element_id).first()
        if result:
            abort(409,message="Duplicate data.")
        args=pre_element_add_args.parse_args()
        element=PreElementModel(element_id=element_id,element_name=args["element_name"])
        db.session.add(element)
        db.session.commit()
        return element,201

    @marshal_with(pre_element_field)
    def patch(self,element_id):
        args=pre_element_add_args.parse_args()
        result=PreElementModel.query.filter_by(element_id=element_id).first()
        if not result:
            abort(404,message="Data not found.")
        if args["element_name"]:
            result.element_name=args["element_name"]
        db.session.commit()
        return result
    
    def delete(self,element_id):
        result=PreElementModel.query.filter_by(element_id=element_id).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class PreElementDate(Resource):
    @marshal_with(pre_element_date_field)
    def get(self,date_id):
        args=pre_element_date_add_args.parse_args()
        if args["date_id"] == 0:   
            result=PreElementDateModel.query.filter_by(start_date>=args["start_date"],start_date<=args["end_date"])
        else:
            result=PreElementDateModel.query.filter_by(date_id=date_id).first()
        if not result:
            abort(404,message="Data not found.")
        return result
    
    @marshal_with(pre_element_date_field)
    def post(self,date_id):
        result=PreElementDateModel.query.filter_by(date_id=date_id).first()
        if result:
            abort(409,message="Duplicate data.")
        args=pre_element_date_add_args.parse_args()
        element=PreElementDateModel(date_id=date_id,start_date=args["start_date"],end_date=args["end_date"],element_id=args["element_id"])
        db.session.add(element)
        db.session.commit()
        return element,201

    @marshal_with(pre_element_date_field)
    def patch(self,date_id):
        args=pre_element_date_add_args.parse_args()
        result=PreElementDateModel.query.filter_by(date_id=date_id).first()
        if not result:
            abort(404,message="Data not found.")
        if args["start_date"]:
            result.start_date=args["start_date"]
        if args["end_date"]:
            result.end_date=args["end_date"]
        if args["element_id"]:
            result.element_id=args["element_id"]
        db.session.commit()
        return result
    
    def delete(self,date_id):
        result=PreElementDateModel.query.filter_by(date_id=date_id).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class Product(Resource):
    @marshal_with(product_field)
    def get(self,product_code):
        result=ProductModel.query.filter_by(product_code=product_code).first()
        if not result:
            abort(404,message="Data not found.")
        return result
    
    @marshal_with(product_field)
    def post(self,product_code):
        result=ProductModel.query.filter_by(product_code=product_code).first()
        if result:
            abort(409,message="Duplicate data.")
        args=product_add_args.parse_args()
        product=ProductModel(product_code=product_code,product_name=args["product_name"],risk_level=args["risk_level"])
        db.session.add(product)
        db.session.commit()
        return product,201

    @marshal_with(product_field)
    def patch(self,product_code):
        args=product_add_args.parse_args()
        result=ProductModel.query.filter_by(product_code=product_code).first()
        if not result:
            abort(404,message="Data not found.")
        if args["product_name"]:
            result.product_name=args["product_name"]
        if args["risk_level"]:
            result.element_id=args["risk_level"]
        db.session.commit()
        return result
    
    def delete(self,product_code):
        result=ProductModel.query.filter_by(product_code=product_code).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class ProductGroup(Resource):
    @marshal_with(product_group_field)    
    def get(self,element_id):
        args=product_group_add_args.parse_args()
        if element_id == 0:                     
            result=ProductGroupModel.query.filter_by(element_id=args["element_id"]).all()
        else:
            result=ProductGroupModel.query.filter_by(element_id=args["element_id"],product_code=args["product_code"]).all()
        if not result:
            abort(404,message="Data not found.")
        return result
   
    @marshal_with(product_group_field)
    def post(self,element_id):
        args=product_group_add_args.parse_args()
        result=ProductGroupModel.query.filter_by(element_id=element_id,product_code=args["product_code"]).first()
        if result:
            abort(409,message="Duplicate data.")
        product=ProductGroupModel(element_id=element_id,product_code=args["product_code"])
        db.session.add(product)
        db.session.commit()
        return product,201

    @marshal_with(product_group_field)
    def patch(self,element_id):
        abort(404,message="Not support.")
        return result
    
    @marshal_with(product_group_field)
    def delete(self,element_id):
        args=product_group_add_args.parse_args()
        result=ProductGroupModel.query.filter_by(element_id=element_id,product_code=args["product_code"]).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

class Avatar(Resource):
    @marshal_with(avatar_field)
    def get(self,avatar_id):
        result=AvatarModel.query.filter_by(avatar_id=avatar_id).first()
        if not result:
            abort(404,message="Data not found.")
        return result
    
    @marshal_with(avatar_field)
    def post(self,avatar_id):
        result=AvatarModel.query.filter_by(avatar_id=avatar_id).first()
        if result:
            abort(409,message="Duplicate data.")
        args=avatar_add_args.parse_args()
        avatar=AvatarModel(avatar_id=avatar_id,avatar_name=args["avatar_name"],avatar_image=args["avatar_image"])
        db.session.add(avatar)
        db.session.commit()
        return avatar,201

    @marshal_with(avatar_field)
    def patch(self,avatar_id):
        args=avatar_add_args.parse_args()
        result=AvatarModel.query.filter_by(avatar_id=avatar_id).first()
        if not result:
            abort(404,message="Data not found.")
        if args["avatar_name"]:
            result.avatar_name=args["avatar_name"]
        if args["avatar_image"]:
            result.avatar_image=args["avatar_image"]
        db.session.commit()
        return result
    
    def delete(self,avatar_id):
        result=AvatarModel.query.filter_by(avatar_id=avatar_id).first()
        if not result:
            abort(404,message="Data not found.")
        db.session.delete(result)
        db.session.commit()
        return 204

#----- Call -----
api.add_resource(User,"/User/<int:user_id>")
api.add_resource(Customer,"/customer/<int:customer_id>")
api.add_resource(UserAvatar,"/userAvatar/<int:user_id>")
api.add_resource(UserPortfolio,"/userPortfolio/<int:user_id>")

api.add_resource(Questionair,"/questionair/<int:question_id>")

api.add_resource(PreElement,"/preElement/<int:element_id>")
api.add_resource(PreElementDate,"/preElementDate/<int:date_id>")

api.add_resource(Product,"/product/<string:product_code>")
api.add_resource(ProductGroup,"/productGroup/<int:element_id>")

api.add_resource(Avatar,"/avatar/<int:avatar_id>")

if __name__ == '__main__':
     app.run(debug=True,port=5000)
