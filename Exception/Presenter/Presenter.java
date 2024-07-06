package Presenter;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import Model.Model;
import View.View;

public class Presenter {

    private String message;
    private String inputString;
    
    private ArrayList<String> list;
    private DateTimeFormatter formatter;
    private LocalDate bd;
    private int phoneNumber;
    private char gender;
    private String family;
    private String strName;
    private String strSurname;

    public Presenter(){
       
       formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy");
    }

   public void setInputString(String value) {
        this.inputString = value;
        String[] strings = inputString.split(" ");
        List<String> L = Arrays.asList(strings);
        this.list = new ArrayList<>(L);
   }

   private boolean checker(){         
        try{
            int n  = size();
            this.bd = dateBD();
            this.phoneNumber = getPhone();
            this.gender = getGender(); 
            this.family = list.get(0);
            this.strName = list.get(1);
            this.strSurname = list.get(2);
        } catch (Exception e) {
            this.message = e.getMessage() ;
            int n = 0;            
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
        if (checker()){
            Model model = new Model();
            model.setFamily(this.family);
            model.setName(this.strName);
            model.setSurname(this.strSurname);
            model.setBirthDate(bd);
            model.setPhone(this.phoneNumber);
            model.setGender(this.gender);
            this.message = model.getMessage();
        }         
        return this.message;
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

   private int getPhone() throws RuntimeException {
        int phone = -1;
        for (int i = 0; i < 5; i++){
            try {
                phone = Integer.parseInt(this.list.get(i));
                this.list.remove(i);
                return phone;
            } catch (NumberFormatException e) {
                phone = -1;
            }
        }
        if (phone == -1){
            throw new RuntimeException("Неправильный формат номера телефона");
        }
        return -1;
    }

    private char getGender() throws RuntimeException {
        char c = '\u0000';
        for (int i = 0; i < 4; i++){
            if (this.list.get(i).equals("f")){
                this.list.remove(i);
                return 'f';
            } else if(this.list.get(i).equals("m")){
                this.list.remove(i);
                return 'm';
            }
        }
        if (c == '\u0000') {
            throw new RuntimeException("Пол неопределён");
        }
        return '\u0000';
    }




   //DateTimeParseException NumberFormatException
}
