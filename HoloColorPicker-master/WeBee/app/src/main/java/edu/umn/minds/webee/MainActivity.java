package edu.umn.minds.webee;

import android.graphics.Color;
import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.appindexing.Thing;
import com.google.android.gms.common.api.GoogleApiClient;
import com.larswerkman.holocolorpicker.ColorPicker;
import com.larswerkman.holocolorpicker.ValueBar;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class MainActivity extends AppCompatActivity implements ColorPicker.OnColorChangedListener, View.OnClickListener {

    private TextView m_TextColor, m_TextColorIndex;
    private ColorPicker m_Picker;
    private ImageButton m_BtnSwitch;
    private boolean m_Status;
    private final boolean STATUS_ON = true;
    private final boolean STATUS_OFF = false;
    private int m_ColorIndex = -1;
    private int m_Color = -1;
    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    private GoogleApiClient client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        m_Picker = (ColorPicker) findViewById(R.id.picker);
        m_Picker.setOnColorChangedListener(this);
        // m_Picker.setShowOldCenterColor(false);
        // m_Picker.setShowOldCenterColor(false);
        m_TextColor = (TextView) findViewById(R.id.tx_color);
        m_TextColorIndex = (TextView) findViewById(R.id.tx_colorIndex);

        m_BtnSwitch = (ImageButton) findViewById(R.id.imageButton);
        m_BtnSwitch.setOnClickListener(this);

        ValueBar valueBar = (ValueBar) findViewById(R.id.valuebar);
        m_Picker.addValueBar(valueBar);

        m_Status = STATUS_OFF;
        m_Picker.setColor(Color.GRAY);
        m_Picker.setOldCenterColor(Color.GRAY);
        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();

        //cp aireplay-ng-color executive file to /mnt
        try {
            String[] cmd_cp = {"su", "-c", "cp /sdcard/webee/aireplay-ng-color /mnt"};
            Runtime.getRuntime().exec(cmd_cp);
            String[] cmd_chmod = {"su", "-c", "chmod 777 /mnt/aireplay-ng-color"};
            Runtime.getRuntime().exec(cmd_chmod);
        }catch (Exception e){
            e.printStackTrace();
            Toast.makeText(MainActivity.this,"Initialization Failed",Toast.LENGTH_SHORT).show();
        }

    }

    @Override
    public void onColorChanged(int color) {
        //Toast.makeText(this, String.valueOf(color), Toast.LENGTH_SHORT).show();
        String alpha = String.format("%02x", Color.alpha(color)),
                red = String.format("%02x", Color.red(color)),
                green = String.format("%02x", Color.green(color)),
                blue = String.format("%02x", Color.blue(color));
        m_TextColor.setText("0x" + red + green + blue);
        m_Picker.setOldCenterColor(color);

        //Log.d("onColorChanged", "0x" + red + green + blue);
        if (m_Status == STATUS_ON) {

            //Get color and quantize
            int Red = Color.red(color);
            int Green = Color.green(color);
            int Blue = Color.blue(color);

            m_Color = color;

            int colorIndex = (Red / 64) * 16 + (Green / 64)*4 + Blue / 64;
            //void turn off
            if(colorIndex == 0){
                colorIndex = 1;
            }
            m_TextColorIndex.setText(String.valueOf(colorIndex));
            if(m_ColorIndex != colorIndex){
                m_ColorIndex = colorIndex;
                // xmitCmd(colorIndex);
                CmdThread thread = new CmdThread(colorIndex);
                thread.start();
            }
        }
    }

    private class CmdThread extends Thread{

        int m_colorIndex;
        public CmdThread(int colorIndex){
            m_colorIndex = colorIndex;
        }
        @Override
        public void run() {
            xmitCmd(m_colorIndex);
        }
    }

    private void xmitCmd(int colorIndex){

        try {
            //enable wlan inteface
            String[] cmd_interface_up = {"su", "-c", "ifconfig wlan0 up"};
            Process process = Runtime.getRuntime().exec(cmd_interface_up);
            /*BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line = null;
            while ((line = bufferedReader.readLine()) != null) {
                System.out.println(line);
            }*/
            process.getInputStream().close();
            process.getOutputStream().close();
            process.getErrorStream().close();
            process.waitFor();
            process.destroy();

            //        System.out.println("------------------------------------------------");

            //switch to channel
            String[] cmd_set_channel = {"su", "-c", "iwconfig wlan0 channel 11"};
            process = Runtime.getRuntime().exec(cmd_interface_up);
           /* bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            line = null;
            while ((line = bufferedReader.readLine()) != null) {
                System.out.println(line);
            }*/
            process.getInputStream().close();
            process.getOutputStream().close();
            process.getErrorStream().close();
            process.waitFor();
            process.destroy();
        //    System.out.println("------------------------------------------------");

            //Just in case
            String[] cmd_chmod = {"su", "-c", "chmod 777 /mnt/aireplay-ng-color"};
            Runtime.getRuntime().exec(cmd_chmod);

            //start transmission
            String cmd_aireplay = "LD_PRELOAD=libfakeioctl.so /mnt/aireplay-ng-color -I " + colorIndex + " -9 wlan0";
            String[] commands = {"su", "-c", cmd_aireplay};
            process = Runtime.getRuntime().exec(commands);
            /*BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line = null;
            while ((line = bufferedReader.readLine()) != null) {
              //  System.out.println(line);
            }*/
            process.getInputStream().close();
            process.getOutputStream().close();
            process.getErrorStream().close();
            process.waitFor();
            process.destroy();

            //        System.out.println("------------------------------------------------");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    @Override
    public void onClick(View v) {

        if (m_Status == STATUS_ON) {
            //light off 5B 00
            m_Status = STATUS_OFF;
            //m_Picker.setColor(Color.GRAY);
            //m_Picker.setOldCenterColor(Color.GRAY);
            m_Picker.setNewCenterColor(Color.GRAY);
            m_BtnSwitch.setImageResource(R.drawable.off);
            m_TextColorIndex.setText("0");
            //m_ColorIndex record the index before we turn it off
            //m_ColorIndex = 0;
            //the 256th cmd is starting with 5B
            xmitCmd(256);

        } else {
            //Light on  05 60
            if(m_ColorIndex < 0 || m_ColorIndex > 256)  {
                m_ColorIndex = 60;
                m_Color = Color.YELLOW;
            }
            m_TextColorIndex.setText(String.valueOf(m_ColorIndex));
            xmitCmd(m_ColorIndex);

            m_Picker.setColor(m_Color);
            m_Picker.setOldCenterColor(m_Color);
            m_BtnSwitch.setImageResource(R.drawable.on);
            m_Status = STATUS_ON;
        }

    }

    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    public Action getIndexApiAction() {
        Thing object = new Thing.Builder()
                .setName("Main Page") // TODO: Define a title for the content shown.
                // TODO: Make sure this auto-generated URL is correct.
                .setUrl(Uri.parse("http://[ENTER-YOUR-URL-HERE]"))
                .build();
        return new Action.Builder(Action.TYPE_VIEW)
                .setObject(object)
                .setActionStatus(Action.STATUS_TYPE_COMPLETED)
                .build();
    }

    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        AppIndex.AppIndexApi.start(client, getIndexApiAction());
    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        AppIndex.AppIndexApi.end(client, getIndexApiAction());
        client.disconnect();
    }
}
