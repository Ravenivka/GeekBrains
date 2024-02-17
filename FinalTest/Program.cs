using System;
using System.Runtime.InteropServices;


class Programm
{

    static char[] SymbolsArray = {' ','!','"','#','$','%','&','(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':',';','<','=',
                            '>','?','@','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                            '[',']','^','_','`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x',
                            'y','z','{','|','}','~','А','Б','В','Г','Д','Е','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц',
                            'Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я','а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у',
                            'ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я','Ё','ё', (char)39, (char)92}; //Перечень допустимых символов

    static string RandomString()
    {
        Random random = new Random();
        int leng = random.Next(1, 10);
        string s = "";
        for (int i = 0; i < leng; i++)
        {
            int index = random.Next(0, SymbolsArray.Length - 1);
            s = s + SymbolsArray[index];
        }
        return s;
    }

    static string[] RandomArray(int wordcount)
    {
        string[] array = new string[wordcount];
        for (int i = 0; i < wordcount; i++)
        {
            array[i] = RandomString();
        }
        return array;
    }

    static string[] CuttedArray(int charcount, string[] array) // блок - схема
    {
        string[] targets = new string[] {};
        foreach (string word in array)
        {
            if(word.Length <= charcount)
            {
                targets = targets.Append(word).ToArray();
            }
        }
        return targets;
    }


    static void Main()
    {
        Console.WriteLine("Для создания массива слов укажите количество элементов:");
        int elementcount;
        try
        {
            elementcount = int.Parse(Console.ReadLine()!);
        }
        catch
        {
            elementcount = 10;
        }

        string[] InputArray = RandomArray(elementcount);
        Console.WriteLine("Массив сгенерирован");
        Console.WriteLine(string.Join("\t ", InputArray));
        Console.WriteLine("Для отсева укажите максимальную длину слова:");
        int maxcharcount;
        try
        {
            maxcharcount = int.Parse(Console.ReadLine()!);
        }
        catch
        {
            maxcharcount = 3;
        }

        string[] TargetArray = CuttedArray(maxcharcount, InputArray);
        Console.WriteLine("Массив отобранных слов:");
        Console.WriteLine(string.Join("\t ", TargetArray));
    }
}
