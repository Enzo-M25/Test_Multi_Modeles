 
from rpy2 import robjects as ro
from rpy2.robjects import StrVector, IntVector
from rpy2.robjects import pandas2ri

class CritereGR4J :
    """
    Regroupe des fonctions différentes de celles du modèle de base (NSE, RMSE, KGE) permettant de calculer des criteres de performances pour le modele GR4J
    """

    def __init__(self):
        
        pandas2ri.activate()

    def define_all(self) -> None:
        """
        Definition de plusieurs criteres non implementes de base dans le package airGR de GR4J
        
        NSE_log
        Biais
        Biais en pourcentage
        """

        r_code = '''
        
        ErrorCrit_NSE_log <- function(InputsCrit, OutputsModel, warnings = TRUE, verbose = TRUE, ...) {
        if (!inherits(OutputsModel, "OutputsModel")) {
            stop("'OutputsModel' must be of class 'OutputsModel'")
        }

        obs <- InputsCrit$Obs
        sim <- OutputsModel$Qsim

        Q_bar <- mean(obs, na.rm = TRUE)
        eps   <- Q_bar / 100
        log_obs <- log(obs + eps)
        log_sim <- log(sim + eps)

        Emod <- sum((log_sim - log_obs)^2, na.rm = TRUE)
        Eref <- sum((log_obs - mean(log_obs, na.rm = TRUE))^2, na.rm = TRUE)

        Crit <- if (Emod == 0 & Eref == 0) 0 else 1 - Emod / Eref

        CritValue <- if (is.numeric(Crit) & is.finite(Crit)) Crit else NA

        if (verbose) {
            message(sprintf("Crit. NSE_log = %.4f", CritValue))
        }

        OutputsCrit <- list(
            CritValue      = CritValue,
            CritName       = "NSE_log",
            CritBestValue  = 1,
            Multiplier     = -1,
            Ind_notcomputed = which(is.na(obs) | is.na(sim))
        )

        class(OutputsCrit) <- c("NSE_log", "ErrorCrit")
        return(OutputsCrit)
        }

        ErrorCrit_Biais <- function(InputsCrit, OutputsModel, ...,
                                      warnings = TRUE, verbose = TRUE) {
          obs <- InputsCrit$Obs
          sim <- OutputsModel$Qsim

          pbias <- 100 * sum(sim - obs, na.rm = TRUE) / sum(obs, na.rm = TRUE)
          list(
            CritName      = "BiasPct",
            CritValue     = pbias,
            CritBestValue = 0,
            Multiplier    = 1
          )
        }

        '''
        ro.r(r_code)