package Presenter;

public class QuantatyException extends RuntimeException {
    
    private String msg;

    public QuantatyException(String msg){
        this.msg = msg;
    }


    public String getMessage ()  {
        return this.msg;
    }
}
