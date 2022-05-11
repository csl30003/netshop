# netshop
Python+Django+MySQL+Redis的网上商城

更改netshop里settings的DATABASES。

要启动支付功能时，去掉在order里urls.py的两条path前的注释，以及views.py里第54行和最后一行的注释，填入支付宝公钥、应用私钥和appid。

启动Redis

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
