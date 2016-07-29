package com.prisma.restapi;

public class ScorePojo {

	private String accountno;
    private String cat_30d;
    private String cat_cv;
    private String cat_icu;
    private String cat_mv;
    private double pred_30d;
    private double pred_cv;
    private double pred_icu;
    private double pred_mv;
    
    public String getAccountno() {
		return accountno;
	}
    
	public void setAccountno(String accountno) {
		this.accountno = accountno;
	}
	
	public String getCat_30d() {
		return cat_30d;
	}
	
	public void setCat_30d(String cat_30d) {
		this.cat_30d = cat_30d;
	}
	
	public String getCat_cv() {
		return cat_cv;
	}
	
	public void setCat_cv(String cat_cv) {
		this.cat_cv = cat_cv;
	}
	
	public String getCat_icu() {
		return cat_icu;
	}
	
	public void setCat_icu(String cat_icu) {
		this.cat_icu = cat_icu;
	}
	
	public String getCat_mv() {
		return cat_mv;
	}
	
	public void setCat_mv(String cat_mv) {
		this.cat_mv = cat_mv;
	}
	
	public double getPred_30d() {
		return pred_30d;
	}
	
	public void setPred_30d(double pred_30d) {
		this.pred_30d = pred_30d;
	}
	
	public double getPred_cv() {
		return pred_cv;
	}
	
	public void setPred_cv(double pred_cv) {
		this.pred_cv = pred_cv;
	}
	
	public double getPred_icu() {
		return pred_icu;
	}
	
	public void setPred_icu(double pred_icu) {
		this.pred_icu = pred_icu;
	}
	
	public double getPred_mv() {
		return pred_mv;
	}
	
	public void setPred_mv(double pred_mv) {
		this.pred_mv = pred_mv;
	}    
	
}
