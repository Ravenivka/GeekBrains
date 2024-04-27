import java.util.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.*;
/*
 * Задание

Реализуйте структуру телефонной книги с помощью HashMap.
Программа также должна учитывать, что в во входной структуре будут повторяющиеся имена с 
разными телефонами, их необходимо считать, как одного человека с разными телефонами. 
Вывод должен быть отсортирован по убыванию числа телефонов.
 
 */


public class program {
    
    private static Map<String, Set<String>> map = new HashMap<>(); // Основной HashMap
    private static Path path = Paths.get("phones.txt");
    private static Scanner scr = new Scanner(System.in);
    private static Map<String, Set<String>> searched =  new HashMap<>(); // результат поиска
    private static String welcome = String.join("\n"
    , "Список команд:"
    , "\t/h - вывод списка команд,"
    , "\t/ac - добавить контакт,"
    , "\t/ap - добавить телефон к контакту,"
    , "\t/d - удалить контакт,"
    , "\t/s - поиск контакта,"
    , "\t/v - вывести все контакты,"
    , "\t/q - выход."
);

    public static void main(String[] args){        
       read();
       System.out.println(welcome);
       System.out.println("Ваша команда");
       boolean flag = true;
       while (flag) {
            String cmd = scr.nextLine();
            switch (cmd) {
                case "/h":
                    System.out.println(welcome);
                    break;
                case "/ac":
                    System.out.println("Введите имя контакта:");
                    String newname = scr.nextLine();
                    addcontact(newname);
                    break;
                case "/ap":
                    System.out.println("Введите имя контакта:");
                    String name = scr.nextLine();
                    addphone(name);
                    break;
                case "/d":
                    System.out.println("Введите имя контакта для удаления:");
                    name = scr.nextLine();
                    map.remove(name);
                    break;
                case "/s":
                    System.out.println("Введите маску поиска:");
                    name = scr.nextLine();
                    searched = search(name);
                    view(searched);
                    break;
                case "/v":
                    sort(map); //сортировка + печать
                    break;
                case "/q":
                    write();
                    flag = false;
                    break;
                default:
                    break;
            }
       }
       
      
    }
   
    private static void read(){ //Чтение из файла, можно было бы и JSON но парсить сложнее без API
        List<String> names = new ArrayList<>();
        List<String> plist = new ArrayList<>();   
        if(Files.exists(path) == false){
            System.out.println("Файл не существует и будет создан при выходе из программы");
        }else{
            try(BufferedReader reader = Files.newBufferedReader(path, Charset.forName("UTF-8"))){
                String currentLine = null;
                while((currentLine = reader.readLine()) != null){
                    if (currentLine.contains("[name]")){
                        String s = currentLine.substring(9);
                        names.add(s);
                    }else if(currentLine.contains("[phones]")){
                        String s = currentLine.substring(11);
                        plist.add(s);
                    }                    
                }
                List<Set<String>> pars = new ArrayList<>();
                for (int i=0; i < plist.size(); i++){
                    String[] array = plist.get(i).split(";");                    
                    //List<String> list = Arrays.asList(array);
                    Set<String> mySet = new HashSet<String>(Arrays.asList(array));
                    pars.add(mySet);                    
                }
                for (int i=0; i < pars.size(); i++){  //Заполнение справочника
                    if(map.containsKey(names.get(i))){
                        Set<String> list = pars.get(i);
                        Set<String> list2 =map.get(names.get(i));
                        Set<String> list3 = new HashSet<String>();
                        list3.addAll(list);
                        list3.addAll(list2);
                        map.put(names.get(i), list3);
                    }else{
                        map.put(names.get(i), pars.get(i));
                    }
                }

                  //System.out.println(map);

            }catch(IOException ex){
                System.out.println(ex);
            }
        }
    }

    public static void addcontact(String contact){
        Set<String> list = new HashSet<String>();        
        newphone(contact, list);
    }
    public static void addphone(String contact){
        Set<String> list = map.get(contact);
        newphone(contact, list);
    }


    private static void newphone(String contact, Set<String> list){    
        boolean cond = true;
        while(cond){
            System.out.println("Котакт " + contact + ". Добавить номер (номер / n)?");
            String n = scr.nextLine();
            if(n.equals("n")){                
                map.put(contact, list);
                cond = false;
            }else{
                if(n.trim() == ""){
                    System.out.println("Недопустимый формат");
                }else{
                    list.add(n);
                }
            }
        }
    }
    private static Map<String, Set<String>> search(String key){
        Map<String, Set<String>> x = new HashMap<>();
        for(String s : map.keySet()){
            if(s.contains(key)){
                x.put(s, map.get(s));
            }
        }
        return x;
    } 
    private static void view(Map<String, Set<String>> x){
        for(String s : x.keySet()){
            Set<String> list = x.get(s);
            System.out.println("Контакт: " + s);
            for (String str : list) {
                System.out.println("\t" + str.trim());
            }
            //for(int i = 0; i < list.size(); i++){
                //System.out.println("\t" + list.get(i).trim());
           // }
        }
    }
    private static void sort(Map<String, Set<String>> X){
        Map<String, Set<String>> Y = new LinkedHashMap<>();
        while (X.size()>0) {
            Map<String, Set<String>> tmp = maxval(X);
            Y.putAll(tmp);
            Set<String> key = tmp.keySet();
            Object[] KeyArray = key.toArray();
            String K = KeyArray[0].toString() ;
            X.remove(K);
        }
        X.putAll(Y);
        view(Y);
    }
    public static Map<String, Set<String>> maxval(Map<String, Set<String>> Z){
        int maxint = 0;
        String K = "";
        for( Map.Entry<String, Set<String>> entry : Z.entrySet() ){
            if (entry.getValue().size() > maxint){
                K = entry.getKey();
                maxint = entry.getValue().size();
            }
        }
        Map<String, Set<String>> V = new HashMap<>();
        V.put(K, Z.get(K) );
        return V;
    }
    public static void write() {
       String st = String.join("");
        for (String s : map.keySet()) {
            String listString = String.join("; ", map.get(s));
            s = "[name] = " + s ;
            listString = "[phones] = " + listString; 
            st = String.join("\n",st,s,listString);
        }           
            try {
                Files.writeString(path, st);                               
            }
            catch (Exception e) {
                System.out.println(e);
            }
    }

}

