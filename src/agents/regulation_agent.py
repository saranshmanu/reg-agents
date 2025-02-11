from ..base import BaseClient


class RegulationAgent(BaseClient):
    def analyze_regulation(self, question: str) -> str:
        return """
        (a) Chemical substance and significant new uses subject to reporting.
            (1) The chemical substance identified as alkanes, C21-34-branched and linear, 
                chloro (PMN P-12-539; CAS No. 1417900-96-9) is subject to reporting under 
                this section for the significant new uses described in paragraph (a)(2) of 
                this section.
            
            (2) The significant new uses are:
                (i) Industrial, commercial, and consumer activities. Requirements as 
                    specified in § 721.80:
                    - (j) manufacture of the PMN substance with less than 1 weight percent 
                    of chlorinated paraffins with an alkyl chain ≤20
                    - (p) aggregate quantity limits: 1,200,000 kg, 14,100,000 kg, 
                    59,100,000 kg, 78,400,000 kg, and 86,100,000 kg of PMN substances 
                    P-12-539, P-13-107, and P-13-109, effective March 19, 2013
                
                (ii) [Reserved]

        (b) Specific requirements.
            (1) Recordkeeping. Recordkeeping requirements as specified in § 721.125 (a), 
                (b), (c), and (i) are applicable to manufacturers and processors of this 
                substance.
            
            (2) Limitations or revocation of certain notification requirements. The 
                provisions of § 721.185 apply to this section.
        """
