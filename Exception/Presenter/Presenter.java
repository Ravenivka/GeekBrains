package Presenter;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import View.View;

public class Presenter {

    private String inputString;
    private View view;
    private ArrayList<String> list;
    private DateTimeFormatter formatter;
    private LocalDate bd;

    public Presenter(View view){
       this.view = view;
       formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy");
    }

   public void setInputString(String value) {
        this.inputString = value;
        String[] strings = inputString.split(" ");
        List<String> L = Arrays.asList(strings);
        this.list = new ArrayList<>(L);
   }

   private boolean checker(){        
        int n;
        try{
            n  = size();
            this.bd = dateBD();
        } catch (Exception e) {
            System.out.println(e);
            n = 0;
            return false;
        } 

        
         
             
        return true;
   }

   private int size() throws QuantatyException{
    int n = -1;
    if (list.size() < 6){
        throw new QuantatyException("Получено меньше данных, чем требуется.");
    } else if (list.size() > 6){
        throw new QuantatyException("Получено больше данных, чем требуется.");       
    }  
    n = list.size();
    //System.out.println(n);
    return n;
   }

   public String getString() { 
        checker();         
        return this.bd.toString();
   }

   
private LocalDate dateBD() throws WrongDate {   
    LocalDate day = null;
    for (int i = 0; i < 6; i++){
        try{
            day = LocalDate.parse(this.list.get(i) , formatter);            
            this.list.remove(i);
            return day;
        } catch (DateTimeParseException e) {
            day = null;
        }
    } 
    if (day == null){
        throw new WrongDate();
    }       
     return null;  
   }



   //DateTimeParseException
}
