
from camera import open_cam  
from drone_movement import control_drone 
from read_barcode import process_barcode  
from read_qrcode import process_qrcode  

def main():
    camera = open_cam()
    
    print("Starting barcode reading...")
    output_file = 'detected_barcodes.txt'
    process_barcode(camera, output_file)

    print("Starting QR code reading...")
    process_qrcode(camera)

    print("Starting drone control...")
    control_drone()

if __name__ == "__main__":
    main()
