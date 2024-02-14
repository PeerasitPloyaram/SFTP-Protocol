# Simple File Transfer Protocol : SFTP
SFTP is a protocol for transfer files from Client to Server in one way (Client to Server Only)

It can transfer file in any types file, such as
-   Text File  -> txt, py, c, ipynb
-   Image FIle -> PNG, JPG, HEIC
-   Executable File
-   Video      -> MKV, MOV

Create Bye Peerasit Ployaram 6410451237

# Thai Document

## SFTP Phases
1. Connection Phase
    - ทำ Establish Connection ระหว่าง Client กับ Server
    - Client สร้าง PCT Packet และส่งไปยัง Server
    - Server รับ PCT Packet และ ส่ง CT Packet กลับไปยัง Client

2. Transfering Phase
    - Client แบ่งFileออกเป็นChunk และสร้างIdสำหรับfileนั้น
    - Client สร้่างPacket ที่มี IDPacket, Chunk
    - Client ส่ง Packet ไปยัง Server
    - Client สร้าง TFC Packet และ ส่งไปยัง Server
        
3. Validate and Compress Phase
    - Server รับPacket และValidate
    - หากถูกต้องCompress Fileออกมา พร้อมส่ง END Packet ไปยัง Clint
    - หากไม่ถูกต้อ ส่ง RTP Packet ไปยังClientและกลับไปทำTransfering Phase ใหม่


<br>

## SFTP Operations and Packet Format
1. PCT คือ PreContact เป็น Packet ที่ใช้ในการขอการเชื่อมต่อ connection ระหว่าง Client กับ Server โดย Client จะส่ง PCT Packet ไปให้ Server เพื่อขอเปิด connection (Establish Connection) (Conection Phase)

    PCT Packet Format

    ```
    +------------+
    | PCT Packet |
    +------------+
    | [PCT]/     |
    | Sequence   |
    +------------+
    ```


    - [PCT]/SequencNumber 
<br>

2. CT คือ Contact เป็น Packet ที่ใช้ในการบอกการเชื่อมต่อระหว่าง Server กับ Client เสร็จสิ้น โดย Server จะเป็นคนส่ง CT Packet ไปให้ Client

    CT Packet Format
    ```
    +--------------+
    |  CT Packet   |
    +--------------+
    | [CT]/        |
    | Sequence + 1 |
    +--------------+
    ```
    - [CT]/SequencNumber + 1
<br>

3. GET คือ Operation ที่บอกว่าเป็นการรับ Packet เข้ามา
    โดย ทั้ง Server และ Client เป็นคนใช้

    ```
    #เช่น GET [PCT]/Sequence, GET [END]/
    ```
<br>

4. PUSH คือ Operation ที่บอกว่าเปฌนการส่ง Packet ออกไป
    โดย ทั้ง Server และ Client เป็นคนใช้
    ```
    #เช่น PUSH [PCT]/Sequence, PUSH [CT]/Sequence + 1, PUSH [TFC]
    ```
<br>

5. Packet คือ Packet หลักที่ใช้ในการส่ง Chunk ของ File จาก Clent ไปยัง Server
    Packet Format
    ```
    +----------------------+
    |        Packet        |
    +----------------------+
    | [PUSH]/              |
    | NumberOfTotalPacket: |
    | packetNumber:        |
    | IDPacket:            |
    | Checksum:            |
    | Payload              |
    +----------------------+
    ```
    - [PUSH]/NumberOfTotalPacket:packetNumber:IDPacket:Checksum:Payload

<br>

6. TFC คือ Transfer Complete เป็น Packet ที่ใช้ในการส่งหลักจากที่ Client ได้ส่งทุก packet ครบแล้ว เพื่อเป็นการบอกว่าจบการ Transfering Phase
    TFC Packet Format
    ```
    +----------------------+
    |      TFC Packet      |
    +----------------------+
    | [TFC]/               |
    | FileName:            |
    | NumberOfTotalPacket: |
    | Id File              |
    +----------------------+
    ```
    - [TFC]/Filename:NumberOfTotalPacket:IdFile
<br>

7. RTP คือ Retransmit Packet เป็น Packet ที่ใช้ในการขอให้ Client ส่ง packet นั้นมาใหม่
    RTP Packet Format
    ```
    +---------------------+
    |     RTP Packet      |
    +---------------------+
    | [RTP]/              |
    | IDPacket:           |
    | ListOfPacketNumber  |
    +---------------------+
    ```
    - [RTP]/IDPacket:/ListOfPacketNumber
<br>

8. END คือ END Packet เป็น Packet ที่ใช้ในการบอกว่าจบการทำงานการส่ง File จาก Client ไปยัง Server ได้สำเร็จ
    END Packet Format
    ```
    +------------+
    | END Packet |
    +------------+
    | [END]/     |
    +------------+
    ```
    - [END]/
<br>

9. ERROR คือ เกิด Error Operationขึ้น
    ```
    [ERROR] ...
    ```
<br>

# English Document
Comming Soon.

# SFTP Arguments
- For server and client use ```-p``` or ```--port``` for change port by manual.
    ```$ python3 server.py --port port```
<br>

- For client can use ```-t``` or ```--test``` for test connection between client and server
```$ python3 client.py -t```

# SFTP Change Port
- SFTP port default are 13000.

- Can change from default port to Others by


```Bash
# Server
python3 server.py -p 35000
#OR
python3 server.py --port 35000


# Client
python3 client.py filename -p 35000
# OR
python3 client.py filename --port 35000

```

# SFTP Client Test
- User ```-t``` or ```--test``` for test connection between Client and Server 
(Connection Phase)
```$ python3 client.py -p 13000 --test```
<br>

- Server
    ```Bash
    $ python3 server.py
    Server startup from 2024-02-14 13:21:21.340716
    ------------------------------------
    -------Wait for Recive Packet-------
    GET [PCT]65
    PUSH [CT]66
    -----------Client Connect-----------
    ```

- Client
    ```Bash
    $ python3 client.py -p 13000 --test
    -----Try to Connect to Server-----
    PUSH [PCT]65
    GET [CT]66
    -----Client Connected To Server-----
    ```

# SFTP Example File Transfer
- Server
```Bash
$ python3 server.py
Server start port: 13000
Server startup from 2024-02-14 14:57:25.372363
------------------------------------
-------Wait for Recive Packet-------
14:58:02 :  GET [PCT]42
14:58:02 :  PUSH [CT]43
-----------Client Connect-----------
14:58:02 :  GET Packet Id[5510] Packet Number [0]
14:58:02 :  GET Packet Id[5510] Packet Number [1]
14:58:02 :  GET Packet Id[5510] Packet Number [2]
14:58:02 :  GET Packet Id[5510] Packet Number [3]
14:58:02 :  GET Packet Id[5510] Packet Number [4]
14:58:02 :  GET Packet Id[5510] Packet Number [5]
14:58:02 :  GET Packet Id[5510] Packet Number [6]
14:58:02 :  GET Packet Id[5510] Packet Number [7]
14:58:02 :  GET Packet Id[5510] Packet Number [8]
14:58:02 :  GET Packet Id[5510] Packet Number [9]
14:58:02 :  GET Packet Id[5510] Packet Number [10]
14:58:02 :  GET Packet Id[5510] Packet Number [11]
14:58:02 :  GET Packet Id[5510] Packet Number [12]
14:58:02 :  GET Packet Id[5510] Packet Number [13]
14:58:02 :  GET Packet Id[5510] Packet Number [14]
14:58:02 :  GET Packet Id[5510] Packet Number [15]
14:58:02 :  GET Packet Id[5510] Packet Number [16]
14:58:02 :  GET Packet Id[5510] Packet Number [17]
14:58:02 :  GET Packet Id[5510] Packet Number [18]
14:58:02 :  GET Packet Id[5510] Packet Number [19]
14:58:02 :  GET Packet Id[5510] Packet Number [20]
14:58:02 :  GET Packet Id[5510] Packet Number [21]
14:58:02 :  GET Packet Id[5510] Packet Number [22]
14:58:02 :  GET Packet Id[5510] Packet Number [23]
14:58:02 :  GET [TFC]-> Transfer Complete.
14:58:02 :  Status: All Packet Has been Validate.
14:58:02 :  Status: Compress Packet to File
14:58:02 :  Status: File has been Create Successfully.
14:58:02 :  PUSH [END]
```

- Client
    ```Bash
    $ python3 client.py ku_study/network/projectProtocol/testing/cat.jpg
    14:58:02 :  -----Try to Connect to Server-----
    14:58:02 :  PUSH [PCT]42
    14:58:02 :  GET [CT]43
    14:58:02 :  -----Client Connected To Server-----
    14:58:02 :  PUSH Packet Id 5510 Number 0
    14:58:02 :  PUSH Packet Id 5510 Number 1
    14:58:02 :  PUSH Packet Id 5510 Number 2
    14:58:02 :  PUSH Packet Id 5510 Number 3
    14:58:02 :  PUSH Packet Id 5510 Number 4
    14:58:02 :  PUSH Packet Id 5510 Number 5
    14:58:02 :  PUSH Packet Id 5510 Number 6
    14:58:02 :  PUSH Packet Id 5510 Number 7
    14:58:02 :  PUSH Packet Id 5510 Number 8
    14:58:02 :  PUSH Packet Id 5510 Number 9
    14:58:02 :  PUSH Packet Id 5510 Number 10
    14:58:02 :  PUSH Packet Id 5510 Number 11
    14:58:02 :  PUSH Packet Id 5510 Number 12
    14:58:02 :  PUSH Packet Id 5510 Number 13
    14:58:02 :  PUSH Packet Id 5510 Number 14
    14:58:02 :  PUSH Packet Id 5510 Number 15
    14:58:02 :  PUSH Packet Id 5510 Number 16
    14:58:02 :  PUSH Packet Id 5510 Number 17
    14:58:02 :  PUSH Packet Id 5510 Number 18
    14:58:02 :  PUSH Packet Id 5510 Number 19
    14:58:02 :  PUSH Packet Id 5510 Number 20
    14:58:02 :  PUSH Packet Id 5510 Number 21
    14:58:02 :  PUSH Packet Id 5510 Number 22
    14:58:02 :  PUSH Packet Id 5510 Number 23
    14:58:02 :  PUSH [TFC]
    14:58:02 :  GET [END]
    14:58:02 :  -----Client Disconnect From Server-----
    ```

# SFTP Case Retransmit Packet Example

- Server
    ```Bash
    $ python3 server.py
    Server start port: 13000
    Server startup from 2024-02-14 15:02:36.789070
    ------------------------------------
    -------Wait for Recive Packet-------
    15:02:42 :  GET [PCT]25
    15:02:42 :  PUSH [CT]26
    -----------Client Connect-----------
    15:02:42 :  GET Packet Id[1557] Packet Number [0]
    15:02:42 :  GET Packet Id[1557] Packet Number [1]
    15:02:42 :  GET Packet Id[1557] Packet Number [2]
    15:02:42 :  GET Packet Id[1557] Packet Number [3]
    15:02:42 :  GET Packet Id[1557] Packet Number [4]
    15:02:42 :  GET [TFC]-> Transfer Complete.
    15:02:42 :  Status: Found Packet File Missing
    15:02:42 :  PUSH [RTP]
    15:02:42 :  GET Packet Id[1557] Packet Number [5]
    15:02:42 :  GET Packet Id[1557] Packet Number [6]
    15:02:42 :  GET Packet Id[1557] Packet Number [7]
    15:02:42 :  GET Packet Id[1557] Packet Number [8]
    15:02:42 :  GET Packet Id[1557] Packet Number [9]
    15:02:42 :  GET Packet Id[1557] Packet Number [10]
    15:02:42 :  GET Packet Id[1557] Packet Number [11]
    15:02:42 :  GET Packet Id[1557] Packet Number [12]
    15:02:42 :  GET Packet Id[1557] Packet Number [13]
    15:02:42 :  GET Packet Id[1557] Packet Number [14]
    15:02:42 :  GET Packet Id[1557] Packet Number [15]
    15:02:42 :  GET Packet Id[1557] Packet Number [16]
    15:02:42 :  GET Packet Id[1557] Packet Number [17]
    15:02:42 :  GET Packet Id[1557] Packet Number [18]
    15:02:42 :  GET Packet Id[1557] Packet Number [19]
    15:02:42 :  GET Packet Id[1557] Packet Number [20]
    15:02:42 :  GET Packet Id[1557] Packet Number [21]
    15:02:42 :  GET Packet Id[1557] Packet Number [22]
    15:02:42 :  GET Packet Id[1557] Packet Number [23]
    15:02:42 :  GET [TFC]-> Transfer Complete.
    15:02:42 :  Status: All Packet Has been Validate.
    15:02:42 :  Status: Compress Packet to File
    15:02:42 :  Status: File has been Create Successfully.
    15:02:42 :  PUSH [END]
    ```
- Client
    ```Bash
    $ python3 client.py ku_study/network/projectProtocol/testing/cat.jpg
    15:02:42 :  -----Try to Connect to Server-----
    15:02:42 :  PUSH [PCT]25
    15:02:42 :  GET [CT]26
    15:02:42 :  -----Client Connected To Server-----
    15:02:42 :  PUSH Packet Id 1557 Number 0
    15:02:42 :  PUSH Packet Id 1557 Number 1
    15:02:42 :  PUSH Packet Id 1557 Number 2
    15:02:42 :  PUSH Packet Id 1557 Number 3
    15:02:42 :  PUSH Packet Id 1557 Number 4
    15:02:42 :  PUSH [TFC]
    15:02:42 :  GET [RTP]<- Packet Missing
    15:02:42 :  PUSH Packet Id 1557 Number 5
    15:02:42 :  PUSH Packet Id 1557 Number 6
    15:02:42 :  PUSH Packet Id 1557 Number 7
    15:02:42 :  PUSH Packet Id 1557 Number 8
    15:02:42 :  PUSH Packet Id 1557 Number 9
    15:02:42 :  PUSH Packet Id 1557 Number 10
    15:02:42 :  PUSH Packet Id 1557 Number 11
    15:02:42 :  PUSH Packet Id 1557 Number 12
    15:02:42 :  PUSH Packet Id 1557 Number 13
    15:02:42 :  PUSH Packet Id 1557 Number 14
    15:02:42 :  PUSH Packet Id 1557 Number 15
    15:02:42 :  PUSH Packet Id 1557 Number 16
    15:02:42 :  PUSH Packet Id 1557 Number 17
    15:02:42 :  PUSH Packet Id 1557 Number 18
    15:02:42 :  PUSH Packet Id 1557 Number 19
    15:02:42 :  PUSH Packet Id 1557 Number 20
    15:02:42 :  PUSH Packet Id 1557 Number 21
    15:02:42 :  PUSH Packet Id 1557 Number 22
    15:02:42 :  PUSH Packet Id 1557 Number 23
    15:02:42 :  PUSH [TFC]
    15:02:42 :  GET [END]
    15:02:42 :  -----Client Disconnect From Server-----
    ```