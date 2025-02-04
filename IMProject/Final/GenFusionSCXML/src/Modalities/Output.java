package Modalities;

import scxmlgen.interfaces.IOutput;

public enum Output implements IOutput{
    


	CHECK("[SPEECH][ver_emails_recentes]"),
	CHECK_BY_PERSON("[SPEECH][ver_emails_por_pessoa]"),
	CHECK_BY_TAG("[SPEECH][ver_emails_por_tag]"),
	TAG("[SPEECH][tag_email]"),
	//SELECT("[SPEECH][selecionar]"),
	//HELP("[SPEECH][help]"),
	MOVE_UP("[SPEECH][move_up]"),
	MOVE_DOWN("[SPEECH][move_down]"), 
    //READ("[GESTURES][READ]"),  
	 

    // ----------------Complementary----------------
    Delete("[FUSION][Delete]"),
    Archive("[FUSION][Archive]"), 

    // ----------------Redundant----------------
    Help("[FUSION][Help]"),
    Read("[FUSION][Read]"),

    // ----------------Single----------------
     
    Up("[GESTURES][Up]"),
    Down("[GESTURES][Down]"), 
    Select("[GESTURES][Select]"), 

    ;
    
    
    
    private String event;

    Output(String m) {
        event=m;
    }
    
    public String getEvent(){
        return this.toString();
    }

    public String getEventName(){
        return event;
    }
}
