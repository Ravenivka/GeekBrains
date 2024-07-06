package Model;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class Model {

    private DateTimeFormatter formatter;
    private LocalDate bd;
    private int phoneNumber;
    private char gender;
    private String family;
    private String strName;
    private String strSurname;
    

    public Model(){
        formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy");
    }

    public void setBirthDate(LocalDate value){
        this.bd = value;
    }

    public void setPhone(int value){
        this.phoneNumber = value;
    }

    public void setGender(char value){
        this.gender = value;
    }

    public void setFamily (String value) {
        this.family = value;
    }

    public void setName(String value){
        this.strName = value;
    }

    public void setSurname (String value){
        this.strSurname = value;
    }

    private String getString() {
        String d = this.bd.format(this.formatter);
        String s = String.format("<%s><%s><%s><%s> <%d><%c>\n", this.family, this.strName, this.strSurname, d, this.phoneNumber, this.gender);
        return s;
    }

    public String getMessage() {
        Recorder recorder = new Recorder(this.getString(), this.family);
        return recorder.Save();
    }

}
