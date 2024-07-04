package Presenter;

public class WrongDate extends RuntimeException {

    public String getMessage(){
        return "Неправильный формат даты";
    }

}
