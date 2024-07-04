package Presenter;

import View.View;

public class Presenter {

    private String inputString;
    private String outString;

    public Presenter(View view){
        inputString = "";
        outString = "";
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

    public void translate(){
        this.outString = this.inputString;
    }

}
