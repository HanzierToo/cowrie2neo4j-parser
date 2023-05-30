# Cowrie2Neo4j Parser
Python script which reads, parses, then stores Cowrie JSON logs into Neo4j. Created as a part of a university project and built for specific task with room for scalability and expandable features. See below for details.

## Quickstart Guide

> This guide assumes you have set up at least one Cowrie instance and one Neo4j instance on Linux servers (or similar). If you do not, please refer to the plethora of online guides available.

 1. Set working directory to wherever you want on the **Cowrie** instance. Normally the script is placed in the cowrie folder.
```console
cowrie@server:~/cowrie$ cd cowrie
cowrie@server:~/cowrie$ git clone https://github.com/HanzierToo/cowrie2neo4j-parser.git
cowrie@server:~/cowrie$ cd cowrie2neo4j-parser
```
 2. Use your preferred editor and load into the cowrie2neo4j-parser.py, this guide opts to use Nano.
```console
cowrie@server:~/cowrie/cowrie2neo4j-parser$ nano cowrie2neo4j-parser.py
```
 3. Find and change the following lines:
```python
# Connect to the Neo4j server -- Replace <BOLT_IP> with your Neo4j instance, and <USERNAME> and <PASSWORD>.
driver = GraphDatabase.driver("bolt://<BOLT_IP>:7687", auth=("<USERNAME>", "<PASSWORD>"))
```
 4. Once configured, run the following command, assuming you followed the guide in terms of file location.
```console
cowrie@server:~/cowrie/cowrie2neo4j-parser$ python3 cowrie2neo4j-parser.py --file ../var/log/cowrie/cowrie.json
```
You should now see that the data from the Cowrie.json has been parsed and stored into your Neo4j instance.
![Example of Cowrie data parsed into Neo4j graph](https://lh3.googleusercontent.com/oJMkYjrUDCK_wIbHxZhL0gjaYr2IxllXwYCvpGB37BOidDffxe07nh8hJYbq1KYt7Z-FN10emoCW11My1KQR_ZcfleLALvy-u9CY0zvLwyBziV3Dg7x40gQUN1RhTXZLqPOeQxKEvbEtDgdWoa58w_rXSe5G81qXrboItlrsgZNlp9Luonl5SvdGzZXPp8Va-H_OLf2TqdiHnXMROt2JxdBlkRamsYrOsDf52zb-grgDDgPgHQWQ95hU55rx0HJPOqNHyTCou3wXE4Luor6Qt7WElw8xV9Itnh-KJyQIdqhHsGvxJfFkps3Bd1oSAetPz4DVzAqRfBKg92nz6kWe0NylV3nUm-aMmKU-qNJ6JPNzZFI1d4ynVf9ng0XaKbuwmRx6dcM-T8d26Gv-Y_gQVMjQFQDL8g2IcAD7hCAs1RxKrwAkNXA4V4lVHkCutIY2cTLdqhGXfGIvNxS6xEfSVWv2ZjSaoEnoGBi7k3j3n9xHs__VallHNtaI5IdH0sOuTwu6teG_tBQ_uvoXoGkzzyo5Eg17UChthSh88fWymoFmwh4OQFbMngqxFdUYqmoqfTrEkJRBy-4yK3c_9ejSzW5QDapDp-oj7KHXjWWiZYgpC53eJgCd91EcP481ffnbAB9oUqcZ65q2vHmI25KjYhO63PYTXkYb4l9i3eqgl2u5EC6dEaoBCoJhPZjo3uwBZXQeaagQyZvo9TefH2icqLmDB-4EurBSG3TPEGShfJfKiqjSIMDNOgt3gnFFTiCIkiFcqSTWBcJNXwc3XZvOnC9Kw2PyoXWamQ81asCUebeaNo_82wykGFPObxhRUebSSkT3WKDXvDwq10YewBWMoDFbXz9bt0D5g9UNglT2iVhztPSjY4MLCET_i1ndWe_wg-WD0sNUDozwEMQjFkilp1s8mNcJi5WYOrBafx0dFdJzfjS5BpWdTh9Hd_CR1TiBkxXWN57GNzWK1QypfSVJ4_qGfhIBY0xRkVjYFZDvf-WQYtZq0K0ZJ7FbuglHv0e7lqK7Zk8k9oE-kXmGwgfxHjIYK8gPyGny7LYa_ZmY-BpfZ9aR9PR1PyOCeUItWCM=w1048-h955-s-no?authuser=0)
For further problems, troubleshooting, or general inquiries, you can contact me on the following:

> Discord: Hanzier#9779  
> Email: hanzierenduing627@gmail.com
