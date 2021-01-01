using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System;

public class ChangePosition : MonoBehaviour
{
    Thread receiveThread; //1
    UdpClient client; //2
    public int port = 3000; //3

    bool processData = false;
    Vector2 dataPosition;
    float nextIdle = 0f;
    public float ignoreDistance = 0.1f; 
    public float idleRate = 5f;

    public float speed = 1f;

    Vector3 target;

    // Start is called before the first frame update
    void Start()
    {
        InitUDP();
        target = new Vector3(0, 0, transform.position.z);
    }

    void Update()
    {
        if (processData)
        {
            Debug.Log("data");
            target = new Vector3(dataPosition.x, dataPosition.y, transform.position.z);
            processData = false;
        }

        if (Vector3.Distance(transform.position, target) > ignoreDistance)
        {
            float step = speed * Time.deltaTime; // calculate distance to move
            transform.position = Vector3.MoveTowards(transform.position, target, step);
        } else {
            nextIdle = Time.time + idleRate;
        }

        if (Time.time > nextIdle)
        {
            target = new Vector3 (0, 0, transform.position.z);
        }
    }

    void InitUDP()
    {
        Debug.Log("UDP Initialized");

        receiveThread = new Thread(new ThreadStart(ReceiveData)); //1 
        receiveThread.IsBackground = true; //2
        receiveThread.Start(); //3
    }

    void ReceiveData()
    {
        client = new UdpClient(port); //1
        while (true) //2
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port); //3
                byte[] data = client.Receive(ref anyIP); //4

                string text = Encoding.UTF8.GetString(data); //5
                //print(">> " + text);
                Debug.Log(text);

                processData = true;
                dataPosition = JsonUtility.FromJson<Vector2>(text);

                //Debug.Log(newPosition);
            }
            catch (Exception e)
            {
                print(e.ToString()); //7
            }
        }
    }
}
