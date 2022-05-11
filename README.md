# netshop
Python+Django+MySQL+Redis的网上商城

功能：用户登录注册，商品展示，商品详情界面，搜索商品，将不同尺寸颜色数量的商品加入购物车，购物车管理，地址管理，形成订单，支付宝支付。

更改netshop里settings的DATABASES。

要启动支付功能时，去掉在order里urls.py的两条path前的注释，以及views.py里第54行和最后一行的注释，填入支付宝公钥、应用私钥和appid。

启动Redis

python manage.py makemigrations<br />
python manage.py migrate<br />
python manage.py runserver<br />

![image](https://user-images.githubusercontent.com/87610378/167757439-b51017a0-5086-44ee-b9b5-3558e9a297d0.png)
![image](https://user-images.githubusercontent.com/87610378/167757510-778a5f22-6242-46fe-988d-44a60c87119d.png)
![image](https://user-images.githubusercontent.com/87610378/167757608-e0772a7f-3733-4ab6-bf14-011a8d0b0da6.png)
![image](https://user-images.githubusercontent.com/87610378/167757669-3a522fe1-6e68-47ff-ad4b-28ef545f09f1.png)
![image](https://user-images.githubusercontent.com/87610378/167757830-93886df7-d124-4223-840e-27b4a10ab2e9.png)
![image](https://user-images.githubusercontent.com/87610378/167757934-de4d7d27-f2a3-4949-b003-6190e0dfc866.png)
![image](https://user-images.githubusercontent.com/87610378/167758022-3823a452-1803-4a76-8225-9b7932f9ce1b.png)
