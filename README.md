# Simple File Transfer Protocol : SFTP
SFTP is a protocol for transfer files from Client to Server

# Thai Document
## SFTP Operations and Packet Format
1. PCT คือ PreContact เป็น packet ที่ใช้ในการขอการเชื่อมต่อ connection ระหว่าง Client กับ Server โดย Client จะส่ง PCT Packet ไปให้ Server เพื่อขอเปิด connection (Establish Connection)

    PCT Packet Format

    +------------+
    | PCT Packet |
    +------------+
    | [PCT]/     |
    | Sequence   |
    +------------+


    - [PCT]/SequencNumber 
<br>

2. CT คือ Contact เป็น packet ที่ใช้ในการบอกการเชื่อมต่อระหว่าง Server กับ Client เสร็จสิ้น โดย Server จะเป็นคนส่ง CT Packet ไปให้ Client

    CT Packet Format
    +--------------+
    |  CT Packet   |
    +--------------+
    | [CT]/        |
    | Sequence + 1 |
    +--------------+
    - [CT]/SequencNumber + 1
<br>

3. GET
4. PUSH

5. TFC
6. RTP
7. END
# English Document
...