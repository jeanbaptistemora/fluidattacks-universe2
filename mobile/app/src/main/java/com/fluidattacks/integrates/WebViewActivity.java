package com.fluidattacks.integrates;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.ImageButton;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.TextView.OnEditorActionListener;


import com.fluidattacks.integrates.webviewtester.R;

public class WebViewActivity extends Activity {
	
	private WebView webview;
	private EditText addressText;
	private ProgressBar loader;
	private String urlToLoad = "https://fluidattacks.com/integrates";
	public static final String USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		setContentView(R.layout.issue_viewer_nav);
		
		loader = (ProgressBar) findViewById(R.id.loader);
		webview = (WebView) findViewById(R.id.webView1);

		webview.getSettings().setJavaScriptEnabled(true);
        webview.getSettings().setDomStorageEnabled(true);
		// enables viewport meta tag
		webview.getSettings().setUseWideViewPort(true);
		webview.getSettings().setUserAgentString(USER_AGENT);
				
		webview.setWebChromeClient(new WebChromeClient(){
			private int mOriginalOrientation;
			private FrameLayout mFullscreenContainer;		
			private CustomViewCallback mCustomViewCallback;
			
			@Override
	    	public void onShowCustomView(View view, WebChromeClient.CustomViewCallback callback) {
	    		mOriginalOrientation = getRequestedOrientation();
	    		FrameLayout decor = (FrameLayout) getWindow().getDecorView();
	    		mFullscreenContainer = new FrameLayout(getBaseContext());
	    		View bgColour = new View(getBaseContext());
	    		bgColour.setBackgroundColor(0xFF000000);
	    		mFullscreenContainer.addView(bgColour, ViewGroup.LayoutParams.MATCH_PARENT);
	    		mFullscreenContainer.addView(view, ViewGroup.LayoutParams.MATCH_PARENT);
	    		decor.addView(mFullscreenContainer, ViewGroup.LayoutParams.MATCH_PARENT);
	    		mCustomViewCallback = callback;
	    		setRequestedOrientation(getRequestedOrientation());
	    	}
			
			@Override
			public void onHideCustomView() {
				FrameLayout decor = (FrameLayout) getWindow().getDecorView();
				decor.removeView(mFullscreenContainer);
				mFullscreenContainer = null;
				mCustomViewCallback.onCustomViewHidden();
				setRequestedOrientation(mOriginalOrientation);
			}
		});
		
		
		webview.setWebViewClient(new WebViewClient(){
			@Override
			public boolean shouldOverrideUrlLoading(WebView view, String url) {
				// TODO Auto-generated method stub
				return false;
			}
			@Override
			public void onPageFinished(WebView view, String url) {
				// TODO Auto-generated method stub
				super.onPageFinished(view, url);
				
				System.out.println("onPageFinished NOW");
				loader.setVisibility(View.GONE);
				
			}
		});
		
		float scale = getResources().getDisplayMetrics().density;
		float width = getResources().getDisplayMetrics().widthPixels;
		float height = getResources().getDisplayMetrics().heightPixels;

		webview.loadUrl(urlToLoad);
		
	}	
	
	public void onActivityResult(int requestCode, int resultCode, Intent intent) {
		loader.setVisibility(View.VISIBLE);
		webview.loadUrl(urlToLoad);
		addressText.setText(urlToLoad);

	}
	
}
