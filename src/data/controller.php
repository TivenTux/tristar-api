						
<?php
#$ip_tristar="0.0.0.0:0000";
#use env var for docker
$ip_tristar=$_SERVER['TRISTAR_ADDRESS'];

$calls=array(
    "Battery Voltage"  =>array("38","V"),
    "Target Voltage"   =>array("51","V"),
	"Charging Current"  =>array("39","A"),
	"Array Voltage"     =>array("27","V"),
	"Array Current"      =>array("29","A"),
	"Output Power"  =>array("58","W"),
	"Sweep Vmp"       =>array("61","V"),
	"Sweep Voc"       =>array("62","V"),
	"Sweep Pmax"      =>array("60","W"),
	"Battery Temp." =>array("37","C"),		
	"Controller Temp." =>array("35","C"),
	"Kilowatt hours"       =>array("56","kWh"),
	"Status"   =>array("50",""),
	"Absorption"   =>array("77","min"),
	"Balance" =>array("78","min"),
	"Float"     =>array("79","min"),
	"Max Energy(daily)" =>array("70","W"),
	"Ampere hours(daily)"=>array("67","Ah"),
	"Watt hours(daily)"=>array("68","Wh"),
	"Max Voltage(daily)" =>array("66","V"),	
	"Max Battery Voltage(daily)"=>array("65","V"),
	"Min Battery Voltage(daily)"=>array("64","V"),
	"Input Power"   =>array("59","W"),
	"LED"   =>array("49","LED"),
	"Battery Poles Voltage"=>array("25","V"),
	"Battery Sensor Voltage"=>array("26","V"),
	);

function get_data($ip,$alo) {
	if (($handle = fopen("http://".$ip."/MBCSV.cgi?ID=1&F=4&AHI=0&ALO=".$alo."&RHI=0&RLO=1", "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
			$u_value[1]=$data[3];  
			$u_value[2]=$data[4];     }
    fclose($handle);
}
Return $u_value;
}


function get_scale($ip,$alo){
$hi=get_data($ip,$alo);
$lo=get_data($ip,$alo+1);
$hi=$hi[2];
$lo=$lo[2];
$scale_factor=$hi.($lo/65535);
return $scale_factor;
}


function get_scaled_value($raw_data,$tristar_unit,$vscale,$iscale){

switch ($tristar_unit) {
	case "V":
	$u_value=$raw_data[1]*256+$raw_data[2];
	$result=(($u_value*$vscale)/32768)/10;
	break;
	
	case "A":
	$u_value=$raw_data[1]*256+$raw_data[2];
	$result=(($u_value*$iscale)/32768)/10;	
	break;
	
	case "W":	
	$u_value=$raw_data[1]*256+$raw_data[2];
	$result=(($u_value*$vscale*$iscale)/131072)/100;
	break;
	
	case "C":	
	$result=$raw_data[2];
	break;
	
	case "kWh":	
	$result=$raw_data[2];
	break;
	
	case "min":	
	$result=($raw_data[1]*256+$raw_data[2])/60;
	break;
	
	case "Ah":	
	$result=($raw_data[1]*256+$raw_data[2])*0.1;
	break;

	case "Wh":	
	$result=($raw_data[1]*256+$raw_data[2]);
	break;
    
	case "LED":
	$result=$raw_data[2];

	$led_state = Array(	"LED_START","LED_START2","LED_BRANCH","Fast blinking green ","Slow blinking Green ","1 blink per second Green ",
	"Lights Green ","Light Green Yellow","Lights Yellow ","UNDEFINED","Blinking Red ","Lights Red","R-Y-G ERROR","R/Y-G ERROR","R/G-Y ERROR",
	"R-Y ERROR (HTD)","R-G ERROR (HVD)","R/Y-G/Y ERROR","G/Y/R ERROR","G/Y/R x 2");
	$result=$led_state[$result];
	break;
	
	default:
	$result=$raw_data[2];
	$charge_state = Array("Start","Night Check","Disconnect","Night","Fault","MPPT","Absorption","Float","Equalize","Slave");
	$result=$charge_state[$result];
	break;
	
}
if(is_numeric($result)) {
return round($result,2);} else {
return $result;
}
}
  

$vscale=get_scale($ip_tristar,0);
$iscale=get_scale($ip_tristar,2);


foreach($calls as $data_record=>$u_value)
  {
  list($alo,$tristar_unit)=$u_value;
  $raw_data=get_data($ip_tristar,$alo);
  echo "<div>" . $data_record . ":" . get_scaled_value($raw_data,$tristar_unit,$vscale,$iscale).$tristar_unit."</div>";
  }


?>


                  
                    
