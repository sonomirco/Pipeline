Node prioritization and clash detection
Several finite element codes do not allow coincident nodes to be defined. Moreover, nodes that are too close together may generate infinitesimally small elements that could lead to ill-conditioning of the FE model. The Bridge Analytical Engine implements automatic clash detection within the Geometric Engine in order to remove redundant or coincident nodes.

In many cases, nodes of different classes clash (eg. a column workpoint is coincident with the workpoint of a bearing seat when projected onto a bent cap frame element). In these cases, the following prioritization is adopted to remove the redundant nodes.

Current nodal hierarchy / prioritization:

Within 6000, greatest 6000 node has priority (Column WP and Bent Cap End Points)

7000 (Bearing Seat – i) 🡨 6000 (Column WP and Bent Cap End Points)

7000 (Bearing Seat – i) 🡨 8000 (Bearing Seat – j)

8000 (Bearing Seat – j) 🡨 6000 (Column WP and Bent Cap End Points)

2000 (Girder Line – i) 🡨 3000 (Girder Line j)

0000 (Girder Soffit -i) 🡨 1000 (Girder Soffit j)

Examples:

If there is a clash between a column WP on bent cap (6000’s node) and any bearing seat node (7000’s or 8000’s), the bearing seat node will be retained, and the 6000’s node will be omitted since it’s redundant.

If there is a clash between the jth  node of one girder (3000’s) and the ith node of another girder (2000’s), the ith  node will be retained, and the 3000’s node will be omitted.

Loading
The following section provides details on loading.

Unless noted otherwise, the engine and the issued example template files aim to implement loading as defined in AASHTO LRFD-9 Section 3.4.

The definition of each load combination, and the specification of the appropriate load factors, is performed within the template files. Please consult Section 2.4 for more information on the template files of each integration.

DC - dead load (Components)
Traffic rail/barrier [KSF or KN/M2]
User can specify a line load barrier weight.

Line Load barrier weights are then divided into line loads where there is an option to distribute them solely to fascia girders or to all girders.

These line loads are applied to the top flange of the girders.

This is defined by the following:

DC_LBW – ibid.

DC_MBW – ibid.

DC_RBW – ibid.

DC_B_DIST – ibid.

Non-structural deck weight [KSF or K/M2]
User can specify the thickness and unit weight of the deck material to be applied as an area load to the plate elements that compose the deck.

Used for non-structural components like stay-in-place forms and appurtenances.

This is defined by the following:

GAMMA_DECK – Weight density of appurtenances, stay-in-place forms etc.
Haunch
If frame elements are used for girders, haunch loads are rendered using line loads at each girder.

If complex – composite girders are used, haunch loads are capture explicitly, since the haunches are modeled as shell elements in the software.

User can specify a haunch weight and dimensions. The total haunch load will be uniformly distributed to each girder as a line load.

This is defined by the following:

GAMMA_HAUNCH – Weight density of haunch.
DW - dead load (wearing surfaces)
User can specify the thickness and unit weight of the deck material to be applied as an area load to the plate elements that compose the deck.

This is defined by the following:

SD_WEAR – Thickness of wearing material, overlays, topping.

GAMMA_WEAR – Weight density for wearing material, overlays, topping.

LL & IM - live load and dynamic allowance
Currently, the engine can only specify a lane set that follows the primary alignment.
Floating lane definition
Floating lanes are the primary means of distributing live lane loads in the engine. For more information, see the integration notes section as implementation can be software specific.

The floating lane set can be defined parametrically using the following set of inputs:

LN_WIDTH – Width of each lane in the floating lane set (12 ft typical).

LN_MARGIN_L – Distance from left edge of deck to face of left barrier or curb stone.

LN_MARGIN_R – Distance from right edge of deck to face of right barrier or curb stone.

NOTE: A manual intervention is currently necessary for CSi Bridge. Please see Section 2.4.1.1.1.

Fixed lane definition
Fixed lanes used for fatigue analysis are currently not featured in the Engine. If this feature is required for a project, please consult the development team.
Dynamic allowance (IM)
Dynamic allowance is included automatically using the features intrinsic to each FEA software.

Since substructure and foundation components are typically designed with loads that exclude the dynamic allowance, independent load sets are created with and without this component.

CE & BR - centrifugal and braking
Similar to the dynamic allowance, CE and BR are included automatically in the vehicle definition based on the features intrinsic to each FEA software.

See integration notes in Section 2.4.

WS & WL - wind on structure and wind on live
Horizontal and vertical components of Wind-on-Structure (WS) and Wind-on-Live Load (WL) are implemented in the CSi Bridge FEA integration in accordance with AASHTO LRFD Table 3.4.1-1.

The vertical component of WS along with the resulting overturning moment is applied as a force couple comprised of (2) distributed loads per span – one per each fascia girder line.

The Engine implements the typical AASHTO wind load cases wherein the angle of attack, magnitude and sense of the wind forces are varied in accordance with the code.

Currently, WS and WL are specified using (10) parameters:

SPEC – The specification used. Currently, this should not be changed since only one code is implemented. (AASHTO LRFD 9th Ed).

PZ_STR_III – Strength III transverse wind pressure per AASHTO.

PZ_STR_IV – Strength IV transverse wind pressure per AASHTO.

PZ_SER_I – Service I transverse wind pressure per AASHTO.

PZ_SER_IV – Service IV transverse wind pressure per AASHTO.

W_SUPERSR – Average width of the superstructure.

H_SUPSTR_ELEV – Exposed height of the superstructure including girders, deck, barriers.

D_COL – Exposed dimension of the column (width or diameter).

D_CAP – Average depth of each bent cap.

A_CAP – Exposed area at the end face of each bent cap.

Application
WS is applied as a distributed load along the facia girders, as well as at the end of the pier cap, and along the height of the columns.

The distributed loads applied to each column and cap are resolved into orthogonal components based upon the skew angle of each bent. These components are in-plane and out-of-plane of the bent.

WL is applied as a distributed transverse load along the fascia girder, along with a distributed moment to capture the eccentricity.

Table 2 and Table 3 list every permutation of wind loading that is considered by the engine for WS and WL.
