# Bot Consumer - Processor..

**La funcionalidad principal de dicho bot es *"consumir"* información proveniente de Ethereum, *"procesarla"* y *"publicarla"* de manera tal que otros procesos ajenos a este puedan acceder a ella y trabajar en relación de la misma.**

En el proceso intervienen una serie de tecnologías:
1. **'Alchemy'** que nos brinda un nodo en la Blockchain de Etehereum, lo cual nos da acceso a información relacionada a las trasacciones llevadas a cabo en ella. 
2. **'Secret Manager'** un servicio de *'AWS'* que nos permite cifrar la *'API_KEY'* de acceso al nodo antes mencionado, y con esto logramos una capa de mayor seguridad en un punto clave como lo es la conexíon con la Blockchain. 

El lenguaje de codificación es **'Python'**. La obtención de la información se hace a traves de una conexión websocket ya que requerimos la información en tiempo real, la cual proviene de una suscripción a un smartcontract en particular que nos interese monitorear.. Luego de recibir los datos, interviene otro servicio *'AWS'*.

3. **'SNS Topic'** es donde se envía la información y queda disponible para otros procesos. 

Todo corriendo dentro de un **'Docker'** containers para brindar una capa de abstracción y siguiendo con el modelo de micro-servicio.
