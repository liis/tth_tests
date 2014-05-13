import ROOT, math

def get_sys_err( sys_hist, nominal_hist ):
    sys_variation = sys_hist.Clone("sys_variation")
    sys_variation.Add(nominal_hist.Scale(-1))

    return sys_variation

def find_sum_sys( h, list_of_sys, hist, nrebin=1):
    """
    h - input file containing systematic histograms
    list_of_hist_names -- list of histograms for sys variation
    return a histogram of the sum in quadrature of syst variations
    """

    processes = ["ttH125", "EWK", "SingleT", "DiBoson", "TTV", "TTJets"]
    nominal = {} # nominal hist
    sub_nominal = {} # -1 * nominal hist
    sys_hist = {}
    err = {}
    err2 = {}
    sum_err2 = {} # squared sum of individual errors
    sys_tot = {} #sqrt(sum_err2)

    for proc in processes:
        histname_nominal = proc + "/" + hist + "_" +  proc
 #       print "Opening nominal histogram: " + histname_nominal
        nominal[proc] = h.Get(histname_nominal)
        nominal[proc].Rebin(nrebin)
        sub_nominal[proc] = nominal[proc].Clone()        
        sub_nominal[proc].Scale(-1)        
            
        for idx, sys in enumerate(list_of_sys):
            sys_hist[proc] = {}
            err[proc] = {}
            err2[proc] = {}

            sys_histname = proc + "_" + sys + "/" +  hist + "_" + proc + "_" + sys
#            print "Opening systematic hist:" + sys_histname
            sys_hist[proc][sys] = h.Get(sys_histname)
            sys_hist[proc][sys].Rebin(nrebin)

            err[proc][sys]= sys_hist[proc][sys].Clone("sys_variation")
            err[proc][sys].Add(sub_nominal[proc])
            
            err2[proc][sys] = err[proc][sys]*err[proc][sys] 

            if idx == 0:
                sum_err2[proc] = err2[proc][sys].Clone("sum_err2")
            else:
                sum_err2[proc].Add(err2[proc][sys])
                        
            #print "mean = " + str(sum_err2[proc].GetMean())
            
        sys_tot[proc] = sum_err2[proc].Clone("sys_tot")
        for ibin in range(sum_err2[proc].GetNbinsX()+1): #loop over all bins and set each bin value to sqrt(err2) (cant sqrt(TH1F))
            isys_sum = sum_err2[proc].GetBinContent(ibin+1)
            sys_tot[proc].SetBinContent(ibin+1, math.sqrt(isys_sum) )

            #print "-------------"
            #print "systot2 = " + str(sys_tot[proc].GetBinContent(ibin + 1)) #Check the consistency
            #print "systot = " + str(math.sqrt(isys_sum))

        i = 0
        for proc in sys_tot:
            if i==0:
                sys_tot_all = sys_tot[proc].Clone()
            else:
                sys_tot_all.Add(sys_tot[proc])
            i+=1

    return sys_tot_all #sys up histogram of the sum of MC contributions
          
