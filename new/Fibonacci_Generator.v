`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: Micah Jeffries and Yale Hone
// 
// Create Date: 11/20/2019 03:11:00 PM
// Design Name: 
// Module Name: Fibonacci_Generator
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: Generates Fibonacci Sequence upon a button press
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module Fibonacci_Generator(
    input BTN,
    input CLK,
    output [7:0] SSEGS,
    output [3:0] AN,
    output LED
    );
    
    //Set up internal wiring
    wire SLOW_CLK, CLR, LD1, LD2, LD3, SEL, UP, RCO;
    wire [1:0] MUX;
    wire [10:0] A,B,C,NEG_C, SUM, MAG_SUM, data_in_reg1;
    
    //Slow down the system clock from 100MHz to ~2Hz
    clk_divider_nbit #(.n(25)) MY_DIV (
        .clockin (CLK), 
        .clockout (SLOW_CLK)          );
    
    //When the button is pressed and the sequence begins, 1 (D0) is hard coded
    //into the register. There is also a special case when the sequence reaches
    //987. This is when 610 (D2) is coded into the register. 610 comes from the
    //output of the second register. Otherwise; the mux outputs the sum of 
    //n-1 & n-2 (D0). Ignore (D3).
    mux_4t1_nb  #(.n(11)) my_4t1_mux  (
        .SEL   (MUX), 
        .D0    (MAG_SUM), 
        .D1    (11'b0000000001), 
        .D2    (C), 
        .D3    (11'b0000000000),
        .D_OUT (data_in_reg1) );
    
    //This register represents n-1 of the fibonacci sequence.
    //Its data input is the mux output.
    reg_nb #(.n(11)) MY_REG1 (
        .data_in  (data_in_reg1), 
        .ld       (LD1), 
        .clk      (SLOW_CLK), 
        .clr      (CLR), 
        .data_out (A)        );
    
    //This register represents n-2 of the fibonacci sequence.
    //Its data input is n-1 from the previous register.
    reg_nb #(.n(11)) MY_REG2 (
        .data_in  (A), 
        .ld       (LD2), 
        .clk      (SLOW_CLK), 
        .clr      (CLR), 
        .data_out (C)        );
    
    //This circuit outputs the positive of the second state register when
    //the fsm is in the addition state. When the fsm is in the subtraction
    //state, this circuit outputs the number's negative. 
    nb_twos_comp #(.n(11)) my_sign_changer (
        .a (C), 
        .a_min (NEG_C)                     ); 
    
    //This mux chooses the positive of the second state register when
    //the fsm is in the addition state. When the fsm is in the subtraction
    //state, this mux chooses the number's negative
    mux_2t1_nb  #(.n(11)) subtraction_2t1_mux  (
        .SEL   (SEL), 
        .D0    (C), 
        .D1    (NEG_C), 
        .D_OUT (B)                             );
    
    //This rca outputs the sum of n-1 & n-2 generating the fibonacci sequence.
    rca_nb #(.n(11)) MY_RCA (
        .a (A), 
        .b (B), 
        .cin (1'b0), 
        .sum (SUM), 
        .co ()              );
    
    //Get the magnitude of the sum from the rca
    mag MY_MAG (
        .A (SUM),
        .B (MAG_SUM) );
    
    //We are generating 16 numbers of the fibonacci sequence in this experiment.
    //Therefore we need a counter that counts up to 16 to keep track of what
    //point we are in the fibonacci sequence.
    cntr_up_clr_nb #(.n(4)) MY_CNTR (
        .clk   (SLOW_CLK), 
        .clr   (1'b0), 
        .up    (UP), 
        .ld    (LD3), 
        .D     (4'b0000), 
        .count (), 
        .rco   (RCO)                );
    
    //This fsm has 4 states: wait (when the button is not pressed),
    //initialize (clear the registers),
    //addition (while the counter counts up to 16), and 
    //subtraction (while the counter counts up to 16 again).
    fsm my_fsm (
        .x_in ({BTN, RCO}),
        .clk (SLOW_CLK),
        .mux (MUX),
        .sel (SEL),
        .clr (CLR),
        .up (UP),
        .ld1 (LD1),
        .ld2 (LD2),
        .ld3 (LD3));
    
    //Display the fibonacci sequence on the seven segment display.
    univ_sseg my_univ_sseg (
        .cnt1 ({3'b000, C}), 
        .cnt2 (7'b0000000), 
        .valid (1'b1), 
        .dp_en (1'b0), 
        .dp_sel (2'b00), 
        .mod_sel (2'b00), 
        .sign (1'b0), 
        .clk (CLK), 
        .ssegs (SSEGS), 
        .disp_en (AN)     );
           
    assign LED = SLOW_CLK;
    
endmodule

module fsm(x_in, clk, mux, sel, clr, up, ld1, ld2, ld3); 
    input  clk;
    input [1:0] x_in; 
    output reg [1:0] mux;
    output reg sel, clr, up, ld1, ld2, ld3;
     
    //- next state & present state variables
    reg [1:0] NS, PS; 
    //- bit-level state representations
    parameter [1:0] st_WAIT=2'b00, st_init=2'b01;
    parameter [1:0] st_ADD=2'b10, st_SUBTRACT=2'b11;
    
    //- status inputs
    wire btn, rco;
    assign rco = x_in[0];
    assign btn = x_in[1]; 

    //- model the state registers
    always @ (posedge clk)
        PS <= NS; 
    
    
    //- model the next-state and output decoders
    always @ (x_in,PS)
    begin
       mux = 2'b00; sel = 1'b0; clr = 1'b0; up = 1'b0; ld1 = 1'b0; ld2 = 1'b0; ld3 = 1'b0;
       case(PS)
          st_WAIT:
          begin
             up = 1'b0; ld1 = 1'b0; ld2 = 1'b0; ld3 = 1'b0;
             if (btn == 0)
                begin
                    mux = 2'b00; sel = 1'b0; clr = 1'b0;
                    NS = st_WAIT;
                end         
             else
                begin
                    mux= 2'b01; sel = 1'b0; clr = 1'b1;
                    NS = st_init;
                end 
          end
             
          st_init:
             begin
                 mux = 2'b01; sel = 1'b0; clr = 1'b0; up = 1'b1; ld1 = 1'b1; ld2 = 1'b0; ld3 = 1'b1;
                 NS = st_ADD;
             end
             
          st_ADD:
             begin
                 up = 1'b1; ld1 = 1'b1; ld2 = 1'b1; ld3 = 1'b0;
                 if (rco == 0)
                    begin
                        mux = 2'b00; sel = 1'b0; clr = 1'b0;
                        NS = st_ADD;
                    end
                 else
                    begin
                        mux = 2'b10; sel = 1'b1; clr = 1'b0;
                        NS = st_SUBTRACT;
                    end
             end
          
          st_SUBTRACT:
          begin
              up = 1'b1; ld1 = 1'b1; ld2 = 1'b1;
              if (rco == 0)
              begin
                  mux = 2'b00; sel = 1'b1; clr = 1'b0;
                  NS = st_SUBTRACT;
              end
           else
              begin
                  mux = 2'b00; sel = 1'b0; clr = 1'b0;
                  NS = st_WAIT;
              end
          end
             
          default: NS = st_WAIT; 
            
          endcase
      end              
endmodule

//Module that determines the magnitude of a given input in RC format
module mag(
    input [10:0] A,
    output [10:0] B
    );
    
    //Set up internal wiring
    wire [10:0] NEG_A;
    
    //Generate the negative of the input A
    nb_twos_comp #(.n(11)) TWOS_COMP (
        .a (A),
        .a_min (NEG_A)     );
        
    //The sign bit of the input determines if A or NEG_A will be the output    
    mux_2t1_nb #(.n(11)) MUX (
        .SEL (A[10]),
        .D0 (A),
        .D1 (NEG_A),
        .D_OUT (B)        );
        
endmodule