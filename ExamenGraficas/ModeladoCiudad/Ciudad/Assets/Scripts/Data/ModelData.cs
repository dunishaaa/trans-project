using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

[Serializable]
public class ModelData
{
    public (int, int) gridSize;
    public List<AgentData> cars;
    public List<AgentData> metrobuses;
    public List<AgentData> pedestrians;
}
