using System;

public class Alter{

public string[] TargetArray(int maxcharnumber, string[] InputArray)
{
    int n = 0;
    foreach(string word in InputArray)
    {
        if(word.Length < maxcharnumber + 1)
        {
            n++;
        }
    }
    string[] Array = new string[n];
    int j = 0;
    for(int i =0; i < InputArray.Length; i++)
    {
        if(InputArray[i].Length < maxcharnumber + 1)
        {
            Array[j] = InputArray[i];
            j++; 
        }
    }
    return Array;
}


}