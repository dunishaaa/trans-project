using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEditor.Rendering;
using UnityEngine;

public class Vehicle : Agent 
{
    public Vehicle()
    {
        speed = 40f;
        rotationSpeed = 200f;
    }
}
