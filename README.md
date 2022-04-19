# Bot Consumer - Processor..

La funcionalidad principal de dicho bot es la de "consumir" información proveniente de un nodo de Ethereum, "procesarla" y publicarla en un tópico SNS de AWS.

En el proceso interviene tecnologías como ser 'Alchemy' que nos brinda un nodo en la Blockchain de Etehereum, 'Secret Manager' un servicio de AWS que nos permite
cifrar nuestro código de acceso al nodo antes mencionado, la obtención de la información se hace a traves de una conexión websocket y una suscripción a un smartcontract en particular. Luego de recibir los datos, los mismo son enviados al servicio de AWS 'SNS Topic' donde esa información queda disponible para otros procesos. 

Todo correctamente 'Dockerizado' para brindar una capa de abstracción. 
El lenguaje de programación para el desarrollo es 'Python'.


