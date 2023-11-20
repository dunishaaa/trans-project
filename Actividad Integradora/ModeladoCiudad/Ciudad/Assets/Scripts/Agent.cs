using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Android;

public abstract class Agent : MonoBehaviour
{
    private int id;

    public Transform currentPosition;
    public Transform targetPosition;

    public int GetId()
    {
        return id;
    }

    public void SetCurrentAndTargetPositions(Transform current, Transform target)
    {
        currentPosition = current;
        targetPosition = target; 
    }

    public void GetData()
    {
        // TODO conexion a la API, probablement hay que crear una interfaz
        print("aksdjfk");
    }

    public abstract void Move();


}
