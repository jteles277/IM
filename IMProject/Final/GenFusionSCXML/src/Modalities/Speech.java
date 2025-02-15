/* 
  *   Speech.java generated by speechmod 
 */   

package Modalities; 

import scxmlgen.interfaces.IModality; 

public enum Speech implements IModality{  


	//CHANGE_COLOR_AZUL("[SPEECH][CHANGE_COLOR][AZUL]",1500),
	//CHANGE_COLOR_VERDE("[SPEECH][CHANGE_COLOR][VERDE]",1500),
	//CHANGE_COLOR_CINZENTO("[SPEECH][CHANGE_COLOR][CINZENTO]",1500),
	//CHANGE_COLOR_VERMELHO("[SPEECH][CHANGE_COLOR][VERMELHO]",1500),
	//CHANGE_COLOR_BRANCO("[SPEECH][CHANGE_COLOR][BRANC]",1500),
	//CHANGE_COLOR_ROSA("[SPEECH][CHANGE_COLOR][ROSA]",1500),
	//CHANGE_COLOR_AMARELO("[SPEECH][CHANGE_COLOR][AMARELO]",1500),
	//CHANGE_COLOR_PRETO("[SPEECH][CHANGE_COLOR][PRETO]",1500),
	//CHANGE_COLOR_LARANJA("[SPEECH][CHANGE_COLOR][LARANJA]",1500),
	//;


	CHECK("[SPEECH][ver_emails_recentes]", 5000),
	CHECK_BY_PERSON("[SPEECH][ver_emails_por_pessoa]", 5000),
	CHECK_BY_TAG("[SPEECH][ver_emails_por_tag]", 5000),
	TAG("[SPEECH][tag_email]", 5000),
	SELECT("[SPEECH][selecionar]", 5000),
	HELP("[SPEECH][help]", 5000),
	MOVE_UP("[SPEECH][move_up]", 5000),
	MOVE_DOWN("[SPEECH][move_down]", 5000), 
	// ----------------Complementary----------------
    Delete("[SPEECH][Delete]", 5000),
    Archive("[SPEECH][Archive]", 5000), 
	;

private String event; 
private int timeout;
Speech(String m, int time) {
	event=m;
	timeout=time;
}
@Override
public int getTimeOut(){
	return timeout;
}
@Override
public String getEventName(){
	return event;
}
@Override
public String getEvName(){
	return getModalityName().toLowerCase() +event.toLowerCase();
}

}
