package Presenter;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import View.View;

public class Presenter {

    private String inputString;
    private String outString;
    private DateTimeFormatter formatter;
    private String[] inputArray; 
    private LocalDate birthDate;

    public Presenter(View view){
        inputString = "";
        outString = "";
        formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy");
        inputArray = new String[0];
        this.birthDate = null;
    }

    public void setInputString(String value){
        this.inputString = value;
    }
    public String getInputString(){
        return this.inputString;
    }

    public void setOutString(String value){
        this.inputString = value;
    }
    public String getOutString(){
        return this.outString;
    }

    public boolean translate(){        
        StringBuilder sb = new StringBuilder();
        Map<Integer, LocalDate> bd;
        String s;
        boolean boo = true;
        try{
            this.inputArray = toArray();            
        } catch (Exception e) {            
            this.outString = "Exception: " + e.getMessage();
            return false;
        }
        try{
            bd = bDate(inputArray);
        } catch (Exception e) {
            this.outString = "Exception: " + e.getMessage();
            return false;
        }
        Entry<Integer, LocalDate> entry = bd.entrySet().iterator().next();
        this.birthDate = entry.getValue()  ; 
        this.inputArray = remove(entry.getKey());
        System.out.println(String.join(" ", inputArray));
        
        
        
        return boo;    
    }

    private String[] toArray() throws QuantatyException{
        String[] s = inputString.split(" ");
        if (s.length < 6){
            throw new QuantatyException("Получено меньше данных, чем требуется.");
        } else if (s.length > 6){
            throw new QuantatyException("Получено больше данных, чем требуется.");
        }
        return s;        
    }

    private Map<Integer, LocalDate> bDate (String[] strings) throws QuantatyException, WrongDate {
        if (inputArray.length == 0) {
            throw new QuantatyException("Пустой массив");
        }
        Map<Integer, LocalDate> mapday = new HashMap<>();
        LocalDate day;                
            for (int i = 0; i < 6; i++) {                
                try{
                    day = LocalDate.parse(inputArray[i], formatter);                                                   
                    mapday.put(i, day);
                } catch (Exception e) {                                        
                    day = null;
                }
            }
            if (mapday.isEmpty()){
                throw new WrongDate();
            }
        return mapday;
    }

    private String[] remove(Integer index){
        String[] strings = new String[this.inputArray.length - 1];
        int j;
        for (int i = 0; i < this.inputArray.length; i++){
           if (i != index){
                if (i < index){
                    j = i;
                } else {
                    j = i - 1;
                }
                strings[j] = inputArray[i];
           }
        }
        return strings;
    }

}
