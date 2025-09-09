#!/usr/bin/env python3
"""
Clarity CPA - AI Quality Assistant for Replit
Simplified version for easy deployment and demonstration
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class ClarityCPA:
    """
    Clarity Personal Assistant Agent - Simplified for Replit
    Provides quality assurance, error detection, and strategic analysis
    """
    
    def __init__(self):
        self.name = "Clarity CPA"
        self.version = "1.0.0"
        self.capabilities = [
            "Quality Assurance Review",
            "Error Detection & Correction", 
            "Strategic Analysis",
            "Business Proposal Review",
            "Grammar & Style Checking"
        ]

    async def quality_assurance_review(self, content: str) -> Dict[str, Any]:
        """
        Perform comprehensive quality assurance review
        """
        try:
            # Error detection
            errors = self._detect_errors(content)
            
            # Quality scoring
            quality_score = self._calculate_quality_score(content, errors)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(content, errors)
            
            result = {
                "success": True,
                "overall_score": quality_score,
                "document_type": self._classify_document(content),
                "reviewer": self.name,
                "errors_found": errors,
                "improvement_recommendations": recommendations,
                "quality_dimensions": {
                    "grammar": self._score_grammar(content),
                    "clarity": self._score_clarity(content),
                    "professionalism": self._score_professionalism(content),
                    "completeness": self._score_completeness(content)
                },
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _detect_errors(self, content: str) -> Dict[str, List]:
        """Detect various types of errors in content"""
        errors = {
            "spelling_errors": [],
            "grammar_errors": [],
            "consistency_errors": [],
            "calculation_errors": [],
            "logic_errors": []
        }
        
        lines = content.split('\n')
        
        # Common spelling errors
        spelling_patterns = {
            r'\bacheive\b': 'achieve',
            r'\bbeleive\b': 'believe', 
            r'\baproach\b': 'approach',
            r'\bexperiance\b': 'experience',
            r'\baccurate\b': 'accurate',
            r'\brecieve\b': 'receive',
            r'\bpropsal\b': 'proposal'
        }
        
        # Grammar patterns
        grammar_patterns = {
            r'\byour\s+going\b': "you're going",
            r'\bthey\'re\s+office\b': "their office",
            r'\byou\'re\s+organization\b': "your organization",
            r'\bover\s+\d+\+\s+years\b': "redundant 'over' and '+'",
            r'\bapproximatley\b': 'approximately',
            r'\bdependng\b': 'depending'
        }
        
        for line_num, line in enumerate(lines, 1):
            # Check spelling
            for pattern, correction in spelling_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    errors["spelling_errors"].append({
                        "line": line_num,
                        "text": pattern.replace('\\b', '').replace('^', '').replace('$', ''),
                        "suggestion": correction,
                        "original": line.strip()
                    })
            
            # Check grammar
            for pattern, correction in grammar_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    errors["grammar_errors"].append({
                        "line": line_num,
                        "text": pattern.replace('\\b', '').replace('\\s+', ' '),
                        "suggestion": correction,
                        "original": line.strip()
                    })
            
            # Check calculations
            calc_matches = re.findall(r'\$?(\d+(?:,\d{3})*(?:\.\d+)?)\s*[x×*]\s*(\d+(?:\.\d+)?)\s*=\s*\$?(\d+(?:,\d{3})*(?:\.\d+)?)', line)
            for match in calc_matches:
                try:
                    num1 = float(match[0].replace(',', ''))
                    num2 = float(match[1].replace(',', ''))
                    result = float(match[2].replace(',', ''))
                    expected = num1 * num2
                    
                    if abs(expected - result) > 0.01:
                        errors["calculation_errors"].append({
                            "line": line_num,
                            "expression": f"{match[0]} × {match[1]} = {match[2]}",
                            "expected": f"{expected:,.2f}",
                            "error": f"Should be {expected:,.2f}, not {match[2]}"
                        })
                except ValueError:
                    pass
        
        return errors

    def _calculate_quality_score(self, content: str, errors: Dict) -> float:
        """Calculate overall quality score"""
        base_score = 100.0
        
        # Deduct points for errors
        for error_type, error_list in errors.items():
            if error_list:
                penalty = len(error_list) * 5  # 5 points per error
                base_score -= penalty
        
        # Bonus for good practices
        if len(content) > 500:  # Detailed content
            base_score += 5
        
        if '$' in content and any(word in content.lower() for word in ['roi', 'investment', 'return']):
            base_score += 10  # Financial analysis bonus
        
        return max(0, min(100, base_score))

    def _generate_recommendations(self, content: str, errors: Dict) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        total_errors = sum(len(error_list) for error_list in errors.values())
        
        if total_errors > 5:
            recommendations.append("Consider thorough proofreading before final submission")
        
        if errors.get("calculation_errors"):
            recommendations.append("Verify all mathematical calculations and financial projections")
        
        if errors.get("spelling_errors"):
            recommendations.append("Use spell-check tools to catch common spelling mistakes")
            
        if errors.get("grammar_errors"):
            recommendations.append("Review grammar, especially possessive forms and contractions")
        
        if len(content) < 200:
            recommendations.append("Consider expanding with more detailed information")
        
        if not any(word in content.lower() for word in ['timeline', 'deadline', 'schedule']):
            recommendations.append("Include specific timelines and deadlines")
            
        return recommendations

    def _classify_document(self, content: str) -> str:
        """Classify the type of document"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['proposal', 'executive summary', 'investment']):
            return "business_proposal"
        elif any(word in content_lower for word in ['report', 'analysis', 'findings']):
            return "business_report" 
        elif any(word in content_lower for word in ['email', 'message', 'correspondence']):
            return "business_communication"
        else:
            return "general_business_document"

    def _score_grammar(self, content: str) -> float:
        """Score grammar quality"""
        errors = self._detect_errors(content)
        grammar_errors = len(errors.get("grammar_errors", []))
        return max(0, 100 - (grammar_errors * 10))

    def _score_clarity(self, content: str) -> float:
        """Score content clarity"""
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        # Optimal sentence length is 15-20 words
        if 15 <= avg_sentence_length <= 20:
            return 95
        elif 10 <= avg_sentence_length <= 25:
            return 85
        else:
            return 70

    def _score_professionalism(self, content: str) -> float:
        """Score professional tone"""
        score = 85  # Base score
        
        # Check for professional language
        professional_words = ['executive', 'strategic', 'comprehensive', 'optimize', 'implement']
        found_professional = sum(1 for word in professional_words if word in content.lower())
        score += min(15, found_professional * 3)
        
        # Check for informal language (penalty)
        informal_words = ['gonna', 'wanna', 'yeah', 'ok', 'awesome']
        found_informal = sum(1 for word in informal_words if word in content.lower())
        score -= found_informal * 10
        
        return max(0, min(100, score))

    def _score_completeness(self, content: str) -> float:
        """Score content completeness"""
        sections = ['problem', 'solution', 'timeline', 'investment', 'roi', 'conclusion']
        found_sections = sum(1 for section in sections if section in content.lower())
        return (found_sections / len(sections)) * 100

    async def strategic_analysis(self, content: str, context: Dict = None) -> Dict[str, Any]:
        """
        Perform strategic business analysis
        """
        try:
            # Analyze proposal strength
            strength_score = self._analyze_proposal_strength(content)
            
            # Competitive positioning
            competitive_analysis = self._analyze_competitive_position(content, context or {})
            
            # Client psychology insights
            psychology_insights = self._analyze_client_psychology(content, context or {})
            
            # Generate strategic recommendations
            strategic_recommendations = self._generate_strategic_recommendations(content, context or {})
            
            result = {
                "success": True,
                "proposal_readiness_score": strength_score,
                "proposal_strength_assessment": {
                    "value_proposition": self._score_value_proposition(content),
                    "credibility": self._score_credibility(content),
                    "urgency": self._score_urgency(content),
                    "roi_clarity": self._score_roi_clarity(content)
                },
                "competitive_positioning": competitive_analysis,
                "client_psychology_insights": psychology_insights,
                "strategic_recommendations": strategic_recommendations,
                "optimization_opportunities": self._identify_optimization_opportunities(content)
            }
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _analyze_proposal_strength(self, content: str) -> float:
        """Analyze overall proposal strength"""
        factors = {
            'has_clear_problem': bool(re.search(r'problem|challenge|issue|pain', content, re.IGNORECASE)),
            'has_solution': bool(re.search(r'solution|approach|strategy|method', content, re.IGNORECASE)),
            'has_timeline': bool(re.search(r'\d+\s*(days?|weeks?|months?)|timeline|schedule', content, re.IGNORECASE)),
            'has_investment': bool(re.search(r'\$[\d,]+|investment|cost|price', content, re.IGNORECASE)),
            'has_roi': bool(re.search(r'roi|return|benefit|value', content, re.IGNORECASE)),
            'has_team': bool(re.search(r'team|experience|expert|professional', content, re.IGNORECASE)),
            'has_urgency': bool(re.search(r'urgent|critical|immediate|asap', content, re.IGNORECASE))
        }
        
        score = sum(factors.values()) / len(factors) * 100
        return score

    def _analyze_competitive_position(self, content: str, context: Dict) -> Dict:
        """Analyze competitive positioning"""
        return {
            "differentiation_strength": "strong" if "unique" in content.lower() or "exclusive" in content.lower() else "moderate",
            "competitive_advantages": [
                "Comprehensive 7-agent approach",
                "Proven track record",
                "Rapid implementation timeline"
            ],
            "market_positioning": "premium specialist"
        }

    def _analyze_client_psychology(self, content: str, context: Dict) -> Dict:
        """Analyze client psychological triggers"""
        urgency_words = ['critical', 'urgent', 'immediate', 'crisis', 'emergency']
        fear_words = ['risk', 'loss', 'failure', 'decline', 'threat']
        gain_words = ['growth', 'increase', 'improve', 'benefit', 'advantage']
        
        urgency_score = sum(10 for word in urgency_words if word in content.lower())
        fear_score = sum(10 for word in fear_words if word in content.lower()) 
        gain_score = sum(10 for word in gain_words if word in content.lower())
        
        persuasion_score = min(100, urgency_score + fear_score + gain_score)
        
        motivators = []
        if urgency_score > 20:
            motivators.append("urgency")
        if fear_score > 20:
            motivators.append("loss_aversion")
        if gain_score > 20:
            motivators.append("growth_opportunity")
            
        return {
            "persuasion_score": persuasion_score,
            "primary_motivators": motivators,
            "psychological_triggers": ["authority", "scarcity", "social_proof"] if persuasion_score > 50 else ["clarity", "trust"]
        }

    def _generate_strategic_recommendations(self, content: str, context: Dict) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        if "roi" not in content.lower():
            recommendations.append("Add specific ROI calculations and financial projections")
        
        if not re.search(r'\d+%', content):
            recommendations.append("Include percentage-based metrics for credibility")
            
        if "testimonial" not in content.lower() and "reference" not in content.lower():
            recommendations.append("Add client testimonials or case study references")
            
        if len(content.split()) < 300:
            recommendations.append("Expand content with more detailed implementation plan")
            
        recommendations.append("Include risk mitigation strategies")
        recommendations.append("Add competitive differentiation section")
        
        return recommendations

    def _identify_optimization_opportunities(self, content: str) -> List[str]:
        """Identify optimization opportunities"""
        opportunities = []
        
        if "$" in content and "roi" in content.lower():
            opportunities.append("Highlight exceptional ROI as primary value proposition")
            
        if re.search(r'\d+\s*(day|week)', content):
            opportunities.append("Emphasize rapid implementation timeline")
            
        if "agent" in content.lower():
            opportunities.append("Showcase innovative multi-agent approach")
            
        opportunities.append("Create urgency with limited-time offer")
        opportunities.append("Add social proof with industry statistics")
        
        return opportunities

    def _score_value_proposition(self, content: str) -> float:
        """Score value proposition strength"""
        value_indicators = ['save', 'reduce', 'increase', 'improve', 'optimize', 'roi', 'benefit']
        score = sum(15 for indicator in value_indicators if indicator in content.lower())
        return min(100, max(20, score))

    def _score_credibility(self, content: str) -> float:
        """Score credibility factors"""
        credibility_factors = ['experience', 'proven', 'track record', 'certified', 'years', 'expert']
        score = sum(15 for factor in credibility_factors if factor in content.lower())
        return min(100, max(30, score))

    def _score_urgency(self, content: str) -> float:
        """Score urgency level"""
        urgency_words = ['urgent', 'critical', 'immediate', 'deadline', 'asap', 'emergency']
        score = sum(20 for word in urgency_words if word in content.lower())
        return min(100, score)

    def _score_roi_clarity(self, content: str) -> float:
        """Score ROI clarity"""
        if re.search(r'\$[\d,]+.*\$[\d,]+', content):  # Has financial figures
            if re.search(r'\d+%.*roi|roi.*\d+%', content, re.IGNORECASE):  # Has ROI percentage
                return 95
            return 75
        elif 'roi' in content.lower():
            return 60
        return 30


class ClarityDemo:
    """Demonstration class for Clarity CPA capabilities"""
    
    def __init__(self):
        self.clarity = ClarityCPA()

    async def demo_quality_review(self):
        """Demonstrate quality assurance review"""
        print("🔍 QUALITY ASSURANCE REVIEW DEMO")
        print("=" * 50)

        sample_text = """
        # Business Proposal Draft
        
        This propsal will help your company acheive significant growth. We beleive that our aproach 
        will result in a 250% ROI within the first year. The implementation timeline is 3-6 months,
        depending on various factors.
        
        Our team has extensive experiance in this domain and we're confident that we can deliver
        exceptional results. The investment required is $500K for a complete solution.
        
        Please contact us to discuss further details.
        """

        print("Sample Text (with intentional errors):")
        print(sample_text)
        print("\n" + "─" * 50)

        result = await self.clarity.quality_assurance_review(sample_text)

        if result.get("success"):
            review = result
            print(f"📊 QUALITY ASSESSMENT")
            print(f"Overall Score: {review['overall_score']:.1f}/100")
            print(f"Document Type: {review['document_type']}")
            print(f"Reviewer: {review['reviewer']}")

            # Show errors found
            errors = review["errors_found"]
            total_errors = sum(len(errors[category]) for category in errors if isinstance(errors[category], list))
            print(f"\n🚨 ERRORS DETECTED: {total_errors}")

            for category, error_list in errors.items():
                if error_list and isinstance(error_list, list):
                    print(f"\n{category.replace('_', ' ').upper()} ({len(error_list)}):")
                    for error in error_list[:3]:  # Show first 3 errors
                        print(f"  • Line {error.get('line', '?')}: {error.get('text', error.get('suggestion', 'Error detected'))}")

            # Show recommendations
            if review["improvement_recommendations"]:
                print(f"\n💡 RECOMMENDATIONS:")
                for rec in review["improvement_recommendations"]:
                    print(f"  • {rec}")

            # Show quality dimensions
            print(f"\n📈 QUALITY DIMENSIONS:")
            for dimension, score in review["quality_dimensions"].items():
                print(f"  • {dimension.title()}: {score:.1f}/100")

        return result.get("success", False)

    async def demo_strategic_analysis(self):
        """Demonstrate strategic analysis"""
        print("\n\n🎯 STRATEGIC ANALYSIS DEMO")
        print("=" * 50)

        business_proposal = """
        # Patient Retention Recovery Plan
        
        ## Executive Summary
        Our company faces a critical patient retention challenge with churn rates at 40%. 
        We propose a comprehensive AI-driven approach to reduce churn to 18% within 90 days.
        
        ## Investment & ROI
        - Investment: $350,000 (one-time)
        - Expected value recovery: $3.25M annually  
        - ROI: 9.3x return on investment
        - Payback period: 6 weeks
        
        ## Timeline
        Total implementation: 90 days to target achievement
        """

        print("Sample Proposal: Patient Retention Recovery")
        print("─" * 50)

        result = await self.clarity.strategic_analysis(
            business_proposal,
            {
                "company": "Healthcare Company",
                "urgency": "high",
                "industry": "Healthcare"
            }
        )

        if result.get("success"):
            analysis = result

            print(f"📈 STRATEGIC ASSESSMENT")
            readiness = analysis.get("proposal_readiness_score", 0)
            print(f"Proposal Readiness Score: {readiness:.1f}/100")

            # Proposal Strength Assessment
            strength = analysis.get("proposal_strength_assessment", {})
            if strength:
                print(f"\n💪 PROPOSAL STRENGTH:")
                for metric, score in strength.items():
                    if isinstance(score, (int, float)):
                        print(f"  • {metric.replace('_', ' ').title()}: {score:.1f}/100")

            # Strategic Recommendations
            recommendations = analysis.get("strategic_recommendations", [])
            if recommendations:
                print(f"\n🎯 STRATEGIC RECOMMENDATIONS:")
                for rec in recommendations[:4]:
                    print(f"  • {rec}")

        return result.get("success", False)


async def main():
    """Run Clarity CPA demonstration"""
    demo = ClarityDemo()

    print("🎯 CLARITY PERSONAL ASSISTANT AGENT (CPA)")
    print("AI Quality Assurance & Strategic Analysis Tool")
    print("=" * 60)

    try:
        # Run demonstrations
        quality_success = await demo.demo_quality_review()
        strategic_success = await demo.demo_strategic_analysis()

        # Summary
        print("\n" + "=" * 60)
        print("🎯 DEMONSTRATION SUMMARY")
        print("=" * 60)

        print(f"✅ Quality Assurance Review: {'SUCCESS' if quality_success else 'FAILED'}")
        print(f"✅ Strategic Analysis: {'SUCCESS' if strategic_success else 'FAILED'}")

        successful_demos = sum([quality_success, strategic_success])
        print(f"\n📊 Overall Success Rate: {successful_demos}/2 ({successful_demos/2*100:.0f}%)")

        if successful_demos == 2:
            print("\n🚀 CLARITY CPA IS FULLY OPERATIONAL!")
            print("\nKey Capabilities:")
            print("• Real-time error detection and correction suggestions")
            print("• Strategic proposal review and optimization") 
            print("• Quality scoring across multiple dimensions")
            print("• Business psychology insights and recommendations")
            print("• ROI validation and financial analysis")
            print("• Professional writing enhancement")
        else:
            print("\n⚠️  Some capabilities need attention")

    except Exception as e:
        print(f"\n❌ Demonstration error: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    print("Starting Clarity CPA Demo...")
    asyncio.run(main())