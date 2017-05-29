Sub Execute_DRUG()
On Error GoTo errHandler

'Scenario Arrays, load in scenarios and scenario coding
Dim ScenarioArray() As Variant
Dim RegionArray() As Variant
Dim RCodeArray() As Variant
Dim IndicationArray() As Variant
Dim ICodeArray() As Variant
Dim LCodeArray() As Variant
Dim TreatmentSheetsArray() As Variant

'Input Arrays - Patient Treatment
Dim ComplianceArray() As Variant
Dim DurationArray() As Variant
Dim InductionPeriodArray() As Variant
Dim InductionDoses_monthArray() As Variant
Dim Doses_monthArray() As Variant
Dim CohortPopArray() As Variant
Dim TreatmentOutputArray() As Variant
Dim PatientOutputArray() As Variant

'****************To be made dynamic************************
'Declare Number of Regions and Number of Indications x Line
Dim RCount As Integer
RCount = 6
Dim ICount As Integer
ICount = 3
Dim SCount As Integer
SCount = RCount * ICount
Dim Sjump As Integer
'**********************************************************

'Load in inputs from VBA sheet; scenario naming and coding
ScenarioArray() = Range("Scenario_Array").Value
RegionArray() = Range("Region_Array").Value
RCodeArray() = Range("RCode_Array").Value
IndicationArray() = Range("Indication_Array").Value
ICodeArray() = Range("ICode_Array").Value
LCodeArray() = Range("LCode_Array").Value
TreatmentSheetsArray() = Range("TreatmentSheets_Array").Value

'input numbers and lookup ranges
ComplianceArray() = Range("Compliance_Array").Value
DurationArray() = Range("Duration_Array").Value
InductionPeriodArray() = Range("InductionPeriod_Array").Value
InductionDoses_monthArray() = Range("InductionDosesMonth_Array").Value
Doses_monthArray() = Range("DosesMonth_Array").Value
CohortPopArray() = Range("CohortPop_Array").Value
TreatmentOutputArray() = Range("TreatmentOutput_Array")
PatientOutputArray() = Range("PatientOutput_Array")

'************************LOOP PATIENT TREATMENT BY REGION***************************
For Region = 1 To RCount
    Sjump = Region * 3
    Worksheets(TreatmentSheetsArray(Sjump, 1)).Activate
    Call Patient_Treatment(DurationArray(), ComplianceArray(), InductionPeriodArray(), InductionDoses_monthArray(), Doses_monthArray(), Region, ICount, CohortPopArray(), TreatmentOutputArray(), PatientOutputArray())
    Dim pctCompl As Integer
    pctCompl = 100 / RCount * Region
    progress pctCompl
Next Region
'************************************************************************************
Exit Sub

errHandler:
    MsgBox ("An error has occured. Please close and re-open the workbook. Check all inputs.")
Exit Sub
End Sub

'****************** PATIENT TREATMENT MODULE - PART 1 **************************************
Sub Patient_Treatment(ByRef DurationArray() As Variant, ByRef ComplianceArray() As Variant, ByRef InductionPeriodArray() As Variant, ByRef InductionDoses_monthArray() As Variant, ByRef Doses_monthArray() As Variant, ByVal Region As Integer, ByVal ICount As Integer, ByRef CohortPopArray() As Variant, ByRef TreatmentOutputArray() As Variant, ByRef PatientOutputArray() As Variant)
On Error GoTo errHandler

'List of months, 1 to 240
Dim Months(1 To 240) As Integer
'CohortID (same as month)
Dim CohortID(1 To 240) As Integer
'TreatmentMatrix, the work horse
Dim TreatmentMatrix(1 To 240, 1 To 240) As Double
'PatientMatrix, the work horses friend
Dim PatientMatrix(1 To 240, 1 To 240) As Double
'Rounding Threshold
Dim Threshold As Double
Threshold = Range("Threshold")(1, 1)

'************************LOOP PATIENT TREATMENT BY INDICATION**************************
For Indication = 1 To ICount

    'Identify which scenario we are in
    Dim Scenario As Integer
    Scenario = (Region - 1) * ICount + Indication

    'Call inputs based on scenario
    Dim Duration As Double
    Duration = DurationArray(Scenario, 1)
    Dim Compliance As Double
    Compliance = ComplianceArray(Scenario, 1)
    Dim InductionPeriod As Integer
    InductionPeriod = InductionPeriodArray(Scenario, 1)
    Dim InductionDoses As Double
    InductionDoses = InductionDoses_monthArray(Scenario, 1)
    Dim PostInductionDoses As Double
    PostInductionDoses = Doses_monthArray(Scenario, 1)

    'Cohort Population - varies by Scenario
    Dim CohortPopOriginal() As Variant
    CohortPopAnnual = Range(CohortPopArray(Scenario, 1)).Value
    Dim CohortPop(1 To 1, 1 To 240) As Variant
    Dim OldPatCount(1 To 240) As Variant

    'Output Array - Total Units per month
    Dim TotDoses(1 To 240) As Variant
    Dim TotPatients(1 To 240) As Variant

'**** for now ****
'CohortPop = CohortPopAnnual

    Dim prevalanceControl As Double

'Apply Matrix Calculations to create matrix of patient population and dosing
    For cohort = 1 To 240
        CohortID(cohort) = cohort
        For month = 1 To 240
            Months(month) = month
            If month = 1 And cohort = 1 Then
                PatientMatrix(1, 1) = CohortPopAnnual(1, 1)
                TreatmentMatrix(1, 1) = CohortPopAnnual(1, 1) * InducionDoses
            ElseIf month = cohort Then
                prevalanceControl = 0
                For y = 1 To cohort - 1
                    prevalanceControl = prevalanceControl + PatientMatrix(y, month)
                Next y
                If prevalanceControl < CohortPopAnnual(1, cohort) Then
                    CohortPop(1, cohort) = CohortPopAnnual(1, cohort) - prevalanceControl
                Else
                    CohortPop(1, cohort) = 0
                End If
            End If
                'If the Month is less than the Cohort # then the cohort population is 0
            If Months(month) < CohortID(cohort) Then
                TreatmentMatrix(cohort, month) = 0
                PatientMatrix(cohort, month) = 0
                'If the month is less than Cohort # + Induction period length then the cohort population is initial patient population
                ElseIf CohortID(cohort) + InductionPeriod > Months(month) Then
                    TreatmentMatrix(cohort, month) = CohortPop(1, cohort) * InductionDoses
                    PatientMatrix(cohort, month) = CohortPop(1, cohort)
                ElseIf Duration = 0 Then
                    TreatmentMatrix(cohort, month) = 0
                    PatientMatrix(cohort, month) = 0
                'If the month is greater than the Cohort # + Induction period, but the decay is less than the rounding threshold then round to 0
                ElseIf CohortPop(1, cohort) * Exp(-1 * (Months(month) - (CohortID(cohort) + InductionPeriod - 1)) / Duration) < Threshold Then
                    TreatmentMatrix(cohort, month) = 0
                    PatientMatrix(cohort, month) = 0
                'Otherwise, decay the population based on e^( - Time on Treatment / Duration), as time on treatment grows population declines
                Else
                    TreatmentMatrix(cohort, month) = CohortPop(1, cohort) * Exp(-1 * (Months(month) - (CohortID(cohort) + InductionPeriod - 1)) / Duration) * PostInductionDoses
                    PatientMatrix(cohort, month) = CohortPop(1, cohort) * Exp(-1 * (Months(month) - (CohortID(cohort) + InductionPeriod - 1)) / Duration)
            End If
            TotDoses(cohort) = TreatmentMatrix(month, cohort) + TotDoses(cohort)
            TotPatients(cohort) = PatientMatrix(month, cohort) + TotPatients(cohort)
        Next month
            TotDoses(cohort) = TotDoses(cohort) * Compliance
    Next cohort

    'Output
    Range(TreatmentOutputArray(Scenario, 1)).Value = TotDoses
    Range(PatientOutputArray(Scenario, 1)).Value = TotPatients

    Erase CohortPop
    Erase TotDoses
    Erase TotPatients
Next Indication
Exit Sub

errHandler:
    MsgBox ("An error has occured. Please close and re-open the workbook. Check all inputs.")
End Sub

Sub progress(pctCompl As Integer)
Progress_Execute.Text.Caption = pctCompl & "% Completed"
Progress_Execute.Bar.Width = pctCompl * 2

DoEvents
End Sub
